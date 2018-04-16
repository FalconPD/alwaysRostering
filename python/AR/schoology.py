""" Allows automated interactions with Schoology
"""

import logging
import json
import uuid
import time
import requests
import http.client
import pprint

pp=pprint.PrettyPrinter()

baseURL = "https://api.schoology.com/v1/"
credentials = json.load(open('../include/credentials.json'))
roles = None
buildings = None
school_id = None

#http.client.HTTPConnection.debuglevel = 1
#logging.basicConfig()
#logging.getLogger().setLevel(logging.DEBUG)
#requests_log = logging.getLogger("requests.packages.urllib3")
#requests_log.setLevel(logging.DEBUG)
#requests_log.propagate = True

def chunks(starting_list, chunk_size):
    """Break a list into smaller lists of size n"""

    for i in range(0, len(starting_list), chunk_size):
        yield starting_list[i:i + chunk_size]

def init():
    global roles, school_id, buildings

    roles = get_roles()
    # We only have 1 school 'Monroe Township Schools'
    school_id = get_schools()['school'][0]['id']
    # inside this school we have lots of buildings...
    buildings = get_buildings()

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

def get_users(roles=[]):
    """Returns a list of users, handling paging. You can optionally specify
    the roles you are looking for"""

    params = None
    if len(roles) > 0:
        params = { "role_ids": map(lookup_role_id, roles) }
    r = requests.get(baseURL + "users", headers=create_header(), params=params)
    r.raise_for_status()
    json_response = r.json()
    users = json_response["user"]
    while ("next" in json_response["links"]):
        next_page_url = json_response["links"]["next"]
        r = requests.get(next_page_url, headers=create_header())
        r.raise_for_status()
        json_response = r.json()
        users += json_response["user"]
    return users

def get_roles():
    """Downloads all of the roles from Schoology"""
    r = requests.get(baseURL + 'roles', headers=create_header())
    r.raise_for_status()
    return r.json()

def get_buildings():
    """Downloads all of the buildings from Schoology"""
    r = requests.get(baseURL + 'schools/' + school_id + '/buildings', headers=create_header())
    r.raise_for_status()
    return r.json()

def get_schools():
    """Downloads all of the schools from Schoology"""
    r = requests.get(baseURL + 'schools', headers=create_header())
    r.raise_for_status()
    return r.json()

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

def bulk_create_update_users(users):
    """Uses the bulk create API call to take a list of users and
    create/update them 50 at a time. Yields the results after each request"""

    params = { 'update_existing': 1 }
    for user_chunk in chunks(users, 50):
        json_data = { 'users': { 'user': user_chunk } }
        r = requests.post(baseURL + 'users', json=json_data, headers=create_header(),
            params=params)
        r.raise_for_status()
        yield r.json()['user']

def create_update_building(title, building_code, address1='', address2='',
    city='Monroe Township', state='NJ', postal_code='08831', country='USA',
    website='', phone='', fax='', picture_url=''):
    """Looks up a building, if it doesn't exist creates it, otherwise updates
    its information. Has some built-in defaults for Monroe"""

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
        r = requests.put(baseURL + 'schools/' + building_id, json=json_data,
            headers=create_header())
    else:
        r = requests.post(baseURL + 'schools/' + school_id + '/buildings',
            json=json_data, headers=create_header())
    r.raise_for_status()
