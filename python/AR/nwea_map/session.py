import asyncio
import aiohttp
import json
import logging
import sys

from AR.nwea_map import constants

class Session():
    """
    A context manager to handle importing profiles in NWEA MAP 
    """
    async def __aenter__(self):
        """
        Creates an aiohttp session and loads the credentials
        """
        self.credentials = json.load(open('../include/credentials.json'))
        self.auth = aiohttp.BasicAuth(login=self.credentials['map']['username'],
            password=self.credentials['map']['password'])
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *exc):
        """
        Closes aiohttp session
        """
        await self.session.close()

    async def request(self, method, url, files=None):
        """
        Perform an HTTP request while submitting our credentials and checking for
        errors
        """
        logging.debug(f"HTTP {method} {url}")
        resp = await self.session.request(method, url, files=files, auth=self.auth)
        logging.debug(f"HTTP RESPONSE {resp.status}")
        if 400 <= resp.status < 500:
            logging.error(f"HTTP {resp.status}")
            sys.exit(1)
        return resp

    async def get(self, url):
        """
        Shortcut for HTTP GET
        """
        return await self.request('GET', url)

    async def post(self, url, files):
        """
        Shortcut for HTTP POST
        """
        return await self.request('POST', url, files)

    async def status(self):
        """
        Gets the status of the last automated import
        """
        resp = await self.get(constants.BASE_URL + 'status')
        return await resp.text()

    async def errors(self):
        """
        Gets the import errors from the last automated import
        """
        resp = await self.get(constants.BASE_URL + 'errors')
        return await resp.text()

    async def upload(self, standard_roster, additional_users):
        pass
