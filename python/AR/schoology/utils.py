"""General utility functions"""
import aiohttp
import asyncio
import logging
import json
import uuid
import time
from AR.schoology import roles, schools, buildings

sem = asyncio.Semaphore(1) # One request at a time
timeout = 1 # wait one second between requests

session = None
baseURL = "https://api.schoology.com/v1/"
credentials = json.load(open('../include/credentials.json'))

async def init(loop):
    """Creates an aiohttp session and loads roles, school_id, and buildings for
    lookups"""

    global session

    session = aiohttp.ClientSession(loop=loop)

    # Get roles and school_id info for lookups
    await asyncio.gather(roles.load(), schools.load())
    
    # Get buildings for lookups (requires school_id)
    await buildings.load()

def make_url(input_str):
    """Adds the BaseURL only if needed"""

    if not input_str.startswith(baseURL):
        return baseURL + input_str
    else:
        return input_str

async def get(endpoint):
    """Performs a HTTP GET and handles the response"""

    url = make_url(endpoint)
    async with sem, session.get(url, headers=create_header()) as resp:
        logging.debug('GET {}'.format(url))
        await asyncio.sleep(timeout)
        await handle_status(resp)
    return resp

async def put(endpoint, json):
    """Performs a HTTP PUT and handles the response"""

    url = make_url(endpoint)
    async with sem, session.put(url, json=json, headers=create_header()) as resp:
        logging.debug('PUT {} json={}'.format(url, json))
        asyncio.sleep(timeout)
        await handle_status(resp)
    return resp

async def post(endpoint, json, params=None):
    """Performs a HTTP POST and handles the response"""

    url = make_url(endpoint)
    async with sem, session.post(url, json=json, params=params, headers=create_header()) as resp:
        logging.debug('POST {} json={} params={}'.format(url, json, params))
        asyncio.sleep(timeout)
        await handle_status(resp)
    return resp

async def delete(endpoint, params=None):
    """Performs a HTTP DELETE and handles the response"""

    url = make_url(endpoint)
    async with sem, session.delete(url, params=params, headers=create_header()) as resp:
        logging.debug('DELETE {} params={}'.format(url, params))
        asyncio.sleep(timeout)
        await handle_status(resp)
    return resp

#def bulk_length_check(items):
#    """Make sure there aren't too many items for a bulk operation"""
#
#    if len(items) > 50:
#        logging.error('Too many items for bulk operation')
#        exit(1)

async def handle_status(resp):
    """Takes a server response and handles errors / warnings"""

    logging.debug('HTTP {}'.format(resp.status))

    if 200 <= resp.status < 300: # 2xx Success
        if resp.status == 207:   # 207 Multi-Status
            response_json = await resp.json()
            if 'user' in response_json:
                responses = response_json['user']
            elif 'course' in response_json:
                responses = response_json['course']
            elif 'section' in response_json:
                responses = response_json['section']
            for line in responses:
                if line['response_code'] != 200:
                    logging.warning('HTTP 207: {}'.format(line))
    elif 300 <= resp.status < 400: # 3xx Redirect
        logging.warning('HTTP {}'.format(resp.status))
    elif 400 <= resp.status < 500: # 4xx Error
        logging.error('HTTP {}'.format(resp.status))
        exit(1)
    elif 500 <= resp.status < 600: # 5xx Server Error
        logging.warning('HTTP {}'.format(resp.status))
    return resp

def create_header():
    return {
        "Authorization":
            'OAuth ' +
            'realm="Schoology API",' +
            'oauth_consumer_key="' + credentials["schoology"]["oauth_consumer_key"] + '",' +
            'oauth_token="",' +
            'oauth_nonce="' + uuid.uuid4().hex + '",' +
            'oauth_timestamp="' + str(int(time.time())) + '",' +
            'oauth_signature_method="PLAINTEXT",' +
            'oauth_version="1.0",' +
            'oauth_signature="' + credentials["schoology"]["oauth_signature"] + '%26"'
    }

async def list_pages(next_link):
    """Generic function for API calls that list things. Yields one page at a
    time"""

    while next_link != None:
        resp = await get(next_link)
        json_response = await(resp.json())
        yield json_response
        next_link = json_response['links']['next'] if ('next' in json_response['links']) else None 
