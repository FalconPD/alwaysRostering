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

async def handle_status(resp):
    """Takes a server response and handles errors / warnings"""

    logging.debug('HTTP {}'.format(resp.status))

    if 200 <= resp.status < 300: # 2xx Success
        if resp.status == 207:   # 207 Multi-Status
            response_json = await resp.json()
            if 'user' in response_json:
                for line in response_json['user']:
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
    """Uses the bulk create API call to take a list of users <= 50 and
    create/update them"""

    logging.debug('Bulk Creating / Updating users in Schoology')
    if len(users) > 50:
        logging.error('Too many users for bulk_create_update_users')
        exit(1)

    params = { 'update_existing': 1 }
    json_data = { 'users': { 'user': users } }
    async with session.post(baseURL + 'users', json=json_data,
        headers=create_header(), params=params) as resp:
        await handle_status(resp)
        response_json = await resp.json()
        return response_json['user']

async def bulk_delete_users(uids, comment='automated delete',
    keep_enrollments=True, email_notification=False):
    """Deletes up to 50 users.
    Defaults: do not notify via email, keeps attendance and grade info, and
    set comment to 'automated delete'"""

    logging.debug('Bulk deleting users in Schoology')
    if len(uids) > 50:
        logging.error('Too many users for bulk_delete_users')
        exit(1)
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


