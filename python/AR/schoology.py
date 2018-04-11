""" Allows automated interactions with Schoology
"""

import logging
import json
import uuid
import time
import requests

baseURL = "https://api.schoology.com/v1/"
credentials = json.load(open('../include/credentials.json'))

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

def get_users():
    r = requests.get(baseURL + "users", headers=create_header())
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
    r = requests.get(baseURL + "roles", headers=create_header())
    r.raise_for_status()
    return r.json()
