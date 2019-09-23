"""
Handles automated interactions with the NWEA MAP system
"""

# System
import asyncio
import aiohttp
import logging
import sys

# alwaysRostering
import AR.credentials as credentials
from AR.nwea_map import constants
from AR.util.token_bucket import TokenBucket

class Session():
    """
    A context manager to handle importing profiles in NWEA MAP
    """
    async def __aenter__(self):
        """
        Creates an aiohttp session, loads the credentials, and sets up a TBF
        """
        self.auth = aiohttp.BasicAuth(login=credentials.map['username'],
            password=credentials.map['password'])
        self.session = aiohttp.ClientSession()
        self.token_bucket = TokenBucket(constants.MAX_TOKENS,
            constants.TOKEN_RATE)
        return self

    async def __aexit__(self, *exc):
        """
        Closes aiohttp session
        """
        await self.session.close()

    async def request(self, method, url, data=None):
        """
        Perform an HTTP request while submitting our credentials and checking for
        errors
        """
        await self.token_bucket.get()
        logging.debug(f"HTTP {method} {url}")
        resp = await self.session.request(method, url, data=data, auth=self.auth)
        logging.debug(f"HTTP RESPONSE {resp.status}")
        if 400 <= resp.status < 500:
            text = await resp.text()
            logging.error(f"HTTP {resp.status} {text}")
            sys.exit(1)
        return resp

    async def get(self, url):
        """
        Shortcut for HTTP GET
        """
        return await self.request('GET', url)

    async def post(self, url, data):
        """
        Shortcut for HTTP POST
        """
        return await self.request('POST', url, data)

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

    async def _upload(self, roster, filename, endpoint):
        data = aiohttp.FormData()
        data.add_field('file',
            open(roster, 'rb'),
            filename=filename),
        resp = await self.post(constants.BASE_URL + endpoint, data=data)
        return await resp.text()

    async def upload_standard(self, standard_roster):
        return await self._upload(standard_roster, 'rf.csv',
            'submit/complete/update')

    async def upload_additional(self, additional_roster):
        return await self._upload(additional_roster, 'others.csv',
            'submit/others')
