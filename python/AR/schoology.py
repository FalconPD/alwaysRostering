""" Allows automated interactions with Schoology
"""

import logging
import json
import uuid
import time
import requests
import http.client
import pprint
import asyncio
import aiohttp

pp=pprint.PrettyPrinter()

baseURL = "https://api.schoology.com/v1/"
credentials = json.load(open('../include/credentials.json'))
roles = None
buildings = None
school_id = None
session = None

def bulk_length_check(items):
    if len(items) > 50:
        logging.error('Too many items for bulk operation')
        exit(1)

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

async def init(loop):
    """Creates an aiohttp session and loads roles, school_id, and buildings for
    lookups"""

    global roles, school_id, session

    session = aiohttp.ClientSession(loop=loop)

    # Get roles and school_id info for lookups
    roles, schools = await asyncio.gather(get_roles(), get_schools())
    school_id = schools['school'][0]['id']
    
    # Get buildings for lookups (requires school_id)
    await load_buildings()

async def load_buildings():
    """This wrapper function allows us to reload the buildings after we
    create/update them"""
    global buildings

    buildings = await get_buildings()

def lookup_role_id(title):
    for role in roles['role']:
        if role['title'] == title:
            return role['id']
    logging.error('Unable to lookup role: {}'.format(title))
    exit(1)

def lookup_building_id(building_code):
    for building in buildings['building']:
        if building['building_code'] == building_code:
            return building['id']
    return None

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

async def get_users(roles=[]):
    """Returns a lists of users one page at a time. You can optionally specify
    the roles you are looking for"""

    logging.debug('Getting users from Schoology')
    params = None
    if len(roles) > 0:
        params = { "role_ids": map(lookup_role_id, roles) }
    async with session.get(baseURL + "users", headers=create_header(), params=params) as resp:
        await handle_status(resp)
        json_response = await resp.json()
        yield json_response['user']
    while ('next' in json_response['links']):
        next_page_url = json_response['links']['next']
        async with session.get(next_page_url, headers=create_header()) as resp:
            await handle_status(resp)
            json_response = await resp.json()
            yield json_response['user']

async def get_roles():
    """Downloads all of the roles from Schoology"""

    logging.debug('Getting roles from Schoology')
    async with session.get(baseURL + 'roles', headers=create_header()) as resp:
        await handle_status(resp)
        return await resp.json()

async def get_buildings():
    """Downloads all of the buildings from Schoology"""

    logging.debug('Getting buildings from Schoology')
    async with session.get(baseURL + 'schools/' + school_id + '/buildings',
        headers=create_header()) as resp:
        await handle_status(resp)
        return await resp.json()

async def get_schools():
    """Downloads all of the schools from Schoology"""

    logging.debug('Getting schools from Schoology')
    async with session.get(baseURL + 'schools', headers=create_header()) as resp:
        await handle_status(resp)
        return await resp.json()

def create_user_object(school_uid, name_first, name_last, email, role):
    """Returns a user object based on the arguments given"""
    return {
        'school_uid': school_uid,
        'name_first': name_first,
        'name_last': name_last,
        'primary_email': email,
        'role_id': lookup_role_id(role),
        'synced': 1
    }

async def bulk_create_update_users(users):
    """Uses the bulk create API call to take a list of users and
    create/update them"""

    logging.debug('Bulk Creating / Updating users in Schoology')
    bulk_length_check(users)

    params = { 'update_existing': 1 }
    json_data = { 'users': { 'user': users } }
    async with session.post(baseURL + 'users', json=json_data,
        headers=create_header(), params=params) as resp:
        await handle_status(resp)
        response_json = await resp.json()
        return response_json['user']

async def bulk_delete_users(uids, comment='automated delete',
    keep_enrollments=True, email_notification=False):
    """Deletes a bulk amount of users.
    Defaults: do not notify via email, keeps attendance and grade info, and
    set comment to 'automated delete'"""

    logging.debug('Bulk deleting users in Schoology')
    bulk_length_check(uids)
    params = {
        'uids': ','.join(map(str, uids)),
        'option_comment': comment,
        'option_keep_enrollments': '1' if keep_enrollments else '0',
        'email_notification': '1' if email_notification else '0'
    }
    async with session.delete(baseURL + 'users', params=params,
        headers=create_header()) as resp:
        await handle_status(resp)
        return await resp.json()

async def create_update_building(title, building_code, address1='', address2='',
    city='Monroe Township', state='NJ', postal_code='08831', country='USA',
    website='', phone='', fax='', picture_url=''):
    """Looks up a building, if it doesn't exist creates it, otherwise updates
    its information. Has some built-in defaults for Monroe"""

    logging.debug('Creating / Updating {}'.format(title))
    json_data = {
        'title': title,
        'building_code': building_code,
        'address1': address1,
        'address2': address2,
        'city': city,
        'state': state,
        'postal_code': postal_code,
        'country': country,
        'website': website,
        'phone': phone,
        'fax': fax,
        'picture_url': picture_url
    }

    building_id = lookup_building_id(building_code)
    if (building_id):
        async with session.put(baseURL + 'schools/' + building_id,
            json=json_data, headers=create_header()) as resp:
            await handle_status(resp)
    else:
        async with session.post(baseURL + 'schools/' + school_id + '/buildings',
            json=json_data, headers=create_header()) as resp:
            await handle_status(resp)

def create_section_object(title, section_school_code):
    """Creates a Schoology Course Section object"""
    
    return {
        'title': title,
        'section_school_code': section_school_code,
        'grading_periods': [1492074755], #TODO: Setup and pull grading periods from SchoolAttendanceCycle in Genesis
        'synced': 1
    }

def create_course_object(building_code, title, course_code, department=None,
    description=None, credits=None, grades=None, subject=None):

    building_id = lookup_building_id(building_code)
    if building_id == None:
        logging.error('Unable to look up building_code {}'.format(building_code))
        exit(1)
    course = {
        'building_id': building_id,
        'title': title,
        'course_code': course_code,
        'synced': 1,
    }
    if department != None:
        course['department'] = department
    if description != None:
        course['description'] = description
    if credits != None:
        course['credits'] = credits
    if grades != None:
        course['credits'] = grades
    if subject != None:
        course['subject'] = subject
    return course

async def bulk_create_update_courses(courses):
    """Takes a list of courses and create/updates them"""

    logging.debug('Bulk creating /updating courses')

    bulk_length_check(courses)

    params = { 'update_existing': 1 }
    json_data = { 'courses': { 'course': courses } }
    async with session.post(baseURL + 'courses/', json=json_data, params=params,
        headers=create_header()) as resp:
        await handle_status(resp)
        return await resp.json()

async def list_pages(next_link):
    """Generic function for API calls that list things. Yields one page at a
    time"""

    while next_link != None:
        async with session.get(next_link, headers=create_header()) as resp:
            await handle_status(resp)
            json_response = await(resp.json())
            yield json_response
            next_link = json_response['links']['next'] if ('next' in
                json_response['links']) else None 

async def list_courses(building_code=None):
    """Lists all the courses. You can optionally specify a building"""

    logging.debug('Listing courses in Schoology')

    # couldnt' figure out a nice, clean way to do this with the params argument
    url = baseURL + 'courses' 
    if building_code:
        building_id = lookup_building_id(building_code)
        if building_id == None:
            logging.error('list_courses: Unable to look up building_code {}'
                .format(building_code))
            exit(1)
        url += '?building_id=' + str(building_id)

    async for response in list_pages(url):
        yield response['course']

async def list_sections(course_id):
    """Lists all the sections for a given course ID."""

    logging.debug('Listing sections in {}'.format(course_id))

    url = baseURL + 'courses/' + str(course_id) + '/sections'

    async for response in list_pages(url):
        yield response['section']

async def bulk_delete_courses(course_ids):
    """Takes a group of course IDs and deletes them"""

    bulk_length_check(course_ids)

    params = { 'course_ids': ','.join(map(str, course_ids)) }
    async with session.delete(baseURL + 'courses', params=params,
        headers=create_header()) as resp: 
        await handle_status(resp)

async def bulk_delete_sections(section_ids):
    """Takes a group of section IDs and deletes them"""

    bulk_length_check(section_ids)

    params = { 'section_ids': ','.join(map(str, section_ids)) }
    async with session.delete(baseURL + 'sections', params=params,
        headers=create_header()) as resp: 
        await handle_status(resp)
