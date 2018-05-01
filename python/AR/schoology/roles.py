"""Functions relating to roles"""
import logging
from AR.schoology import utils

roles = None

async def load():
    """Loads the roles cache"""
    global roles

    roles = await list()

def lookup_id(title):
    """Check our internal list of roles to look up the ID"""

    for role in roles['role']:
        if role['title'] == title:
            return role['id']
    logging.error('Unable to lookup role: {}'.format(title))
    exit(1)

async def list():
    """Downloads all of the roles from Schoology"""

    resp = await utils.get('roles')
    return await resp.json()
