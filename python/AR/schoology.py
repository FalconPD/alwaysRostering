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
    global roles

    roles = get_roles()

def lookup_role_id(title):
    for role in roles["role"]:
        if role['title'] == title:
            return role['id']
    logging.error("Unable to lookup role: {}".format(title))
    exit(1)

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

def create_user_object(school_uid, name_first, name_last, email, role):
    """Returns a user object based on the arguments given"""
    return {
        'school_uid': school_uid,
        'name_first': name_first,
        'name_last': name_last,
        'primary_email': email,
        'role_id': lookup_role_id(role)
    }

def bulk_create_update(users):
    """Uses the bulk create API call to take a list of users and
    create/update them 50 at a time"""

    params = { 'update_existing': 1 }
    user_responses = []
    for user_chunk in chunks(users, 50):
        json_data = { 'users': { 'user': user_chunk } }
        r = requests.post(baseURL + 'users', json=json_data, headers=create_header(),
            params=params)
        r.raise_for_status()
        user_responses += r.json()['user']
    return user_responses
