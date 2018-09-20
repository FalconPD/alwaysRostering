import aiohttp
import asyncio
import logging
import json
import uuid
import time
from AR.schoology import constants
from AR.schoology.grading_periods import GradingPeriods 
from AR.schoology.schools import Schools
from AR.schoology.roles import Roles
from AR.schoology.buildings import Buildings
from AR.schoology.users import Users
from AR.schoology.courses import Courses
from AR.schoology.enrollments import Enrollments
from AR.schoology.course_sections import CourseSections

class Session():
    """
    A context manager to abstract loading of lookup tables and session
    management
    """
    sem = asyncio.Semaphore(constants.HTTP_MAX_REQUESTS)
    credentials = json.load(open(constants.CREDENTIALS_PATH))

    async def __aenter__(self):
        """
        Creates an aiohttp session and loads helper classes
        """
        self.session = aiohttp.ClientSession()

        # These generate some web traffic
        self.Schools = await Schools.create(self) # school_id needed first
        (self.GradingPeriods, self.Buildings, self.Roles) = await asyncio.gather(
            GradingPeriods.create(self), Buildings.create(self),
            Roles.create(self))

        # These do not
        self.Users = await Users.create(self)
        self.Courses = await Courses.create(self)
        self.Enrollments = await Enrollments.create(self)
        self.CourseSections = await CourseSections.create(self)

        return self

    async def __aexit__(self, *exc):
        await self.session.close()

    def create_header(self):
        return {
            "Authorization":
                'OAuth ' +
                'realm="Schoology API",' +
                'oauth_consumer_key="' + self.credentials["schoology"]["oauth_consumer_key"] + '",' +
                'oauth_token="",' +
                'oauth_nonce="' + uuid.uuid4().hex + '",' +
                'oauth_timestamp="' + str(int(time.time())) + '",' +
                'oauth_signature_method="PLAINTEXT",' +
                'oauth_version="1.0",' +
                'oauth_signature="' + self.credentials["schoology"]["oauth_signature"] + '%26"'
        }

    async def request(self, method, endpoint, json=None, params=None):
        """
        Perform a HTTP request with throttling, error checking, and retries
        """
        # Add the BASE_URL if needed
        url = endpoint if endpoint.startswith(constants.BASE_URL) else (constants.BASE_URL + endpoint)
      
        # Retry loop
        retries = 0
        while True:
            # Get a semaphore and perform the request
            async with self.sem, self.session.request(method, url, params=params, json=json,
                headers=self.create_header()) as resp:

                logging.debug('HTTP {} {} params={} json={}'.format(method, url, params,
                    json))

                await asyncio.sleep(constants.HTTP_WAIT)

                logging.debug('HTTP RESPONSE {}'.format(resp.status))
                if 200 <= resp.status < 300: # 2xx Success
                    if resp.status == 207:   # 207 Multi-Status
                        response_json = await resp.json()
                        responses = []
                        if 'user' in response_json:
                            responses += response_json['user']
                        if 'course' in response_json:
                            for course in response_json['course']:
                                sections = course.pop('sections', None)
                                responses.append(course)
                                if sections != None:
                                    responses += sections['section']
                        for response in responses:
                            if response['response_code'] != 200:
                                logging.warning('HTTP 207: {}'.format(response))
                    return resp
                elif 300 <= resp.status < 400: # 3xx Redirect
                    logging.warning('HTTP {}'.format(resp.status))
                    return resp
                elif 400 <= resp.status < 500: # 4xx Error
                    logging.error('HTTP {}'.format(resp.status))
                    exit(1)
                elif 500 <= resp.status < 600: # 5xx Server Error
                    logging.warning('HTTP {}'.format(resp.status))
                    if retries >= 2:
                        logging.error('Too many retries, exiting')
                        exit(1)
            retries += 1
            logging.warning('Retry {}')

    async def get(self, endpoint, params=None):
        """
        Shortcut for HTTP GET
        """
        return await self.request('GET', endpoint, params=params) 

    async def put(self, endpoint, params=None, json=None):
        """
        Shortcut for HTTP PUT
        """
        return await self.request('PUT', endpoint, params=params, json=json) 

    async def post(self, endpoint, params=None, json=None):
        """
        Shortcut for HTTP POST
        """
        return await self.request('POST', endpoint, params=params, json=json)

    async def delete(self, endpoint, params=None):
        """
        Shortcut for HTTP DELETE
        """
        return await self.request('DELETE', endpoint, params=params)

    async def list_pages(self, next_link):
        """
        Generic function for API calls that list things. Yields one page at a
        time
        """
        while next_link != None:
            resp = await self.get(next_link)
            json_response = await(resp.json())
            yield json_response
            next_link = json_response['links']['next'] if ('next' in json_response['links']) else None 
