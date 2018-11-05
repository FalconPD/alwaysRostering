from AR.atlas import constants
from AR.atlas.id_map import ID_Map
from AR.atlas.login_mixin import LoginMixin
from AR.atlas.users_mixin import UsersMixin
import json
import aiohttp
import logging
import sys
import csv

class Session(LoginMixin, UsersMixin):
    """
    A context manager to handle logging in, loading users, loading the ID map,
    saving the ID map etc.
    """
    session = None # our aiohttp session
    id_map = None # maps Atlas IDs to Genesis IDs
    users = {}

    async def __aenter__(self, map_file):
        """
        Creates an aiohttp session, logs in, gets a list of users, loads the
        map
        """
        self.session = aiohttp.ClientSession()
        await self.login()
        self.id_map = ID_Map(map_file)
        await self.load_users()
        return self

    async def __aexit__(self, *exc):
        """
        Closes aiohttp session, writes map
        """
        await self.session.close()
        self.id_map.save()

    async def request(self, method, url, json, params, data, allow_redirects):
        """
        Perform an HTTP request and do some error checking
        """
        logging.debug(
            "HTTP {} {} json={} params={} data={} allow_redirects={}".format(
            method, url, json, params, data, allow_redirects)
        )
        resp = await self.session.request(method, url, json=json, params=params,
            data=data, allow_redirects=allow_redirects)
#            proxy='http://localhost:8888', verify_ssl=False)
        logging.debug('HTTP RESPONSE {}'.format(resp.status))
        if resp.status >= 400:
            logging.error('HTTP {}'.format(resp.status))
            sys.exit(1)
        return resp

    async def post(self, url, json=None, params=None, data=None,
        allow_redirects=True):
        """
        Shortcut for HTTP POST
        """
        return await self.request('POST', url, json, params, data,
            allow_redirects)

    async def get(self, url, params=None, allow_redirects=True):
        """
        Shortcut for HTTP GET
        """
        return await self.request('GET', url, None, params, None,
            allow_redirects)
