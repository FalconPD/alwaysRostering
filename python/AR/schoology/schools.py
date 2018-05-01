"""Functions relating to schools"""
import logging
from AR.schoology import utils

school_id = None

async def load():
    """Loads the schools"""

    global school_id

    schools = await list()
    school_id = schools['school'][0]['id']

async def list():
    """Downloads all of the schools from Schoology"""

    resp = await utils.get('schools')
    return await resp.json()
