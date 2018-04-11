"""Allows automated interactions with MyLearningPlan.com.
"""

import logging
import asyncio
import aiohttp
import json
import pprint
pp = pprint.PrettyPrinter(indent=2)

baseURL = 'https://www.mylearningplan.com'
credentials = json.load(open('../include/credentials.json'))

async def run(loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        print('Logging in to MyLearningPlan')
        await login(session=session)

async def login(session):
    #TODO: Use selenium to login and then pass the cookies to aiohttp
    #https://stackoverflow.com/questions/29563335/how-do-i-load-session-and-cookies-from-selenium-browser-to-requests-library-in-p

    """Login and get session cookie.

    Uses the username and password from credentials.json.
    """

    logging.debug("Gathering cookies and redirected url.")
    url = baseURL + '/mvc/login'
    async with session.get(url) as resp:
        assert resp.status == 200
        url = resp.url
        idsrv_xsrf = resp.cookies['idsrv.xsrf'].value

    username = credentials['mlp']['username']
    password = credentials['mlp']['password']
    logging.debug("Logging in as {}".format(username))
    data = {
        'idsrv.xsrf': idsrv_xsrf,
        'Password': credentials['mlp']['password'],
        'Username': credentials['mlp']['username']
    }
    async with session.post(url, data=data) as resp:
        assert resp.status == 200
        print(await resp.text())
