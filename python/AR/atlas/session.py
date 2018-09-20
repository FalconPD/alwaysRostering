from AR.atlas import constants
from AR.atlas import Users
import json
import aiohttp
import logging
import pprint

pp=pprint.PrettyPrinter(indent=4)

class Session():
    """
    A context manager to handle logging in, loading users, etc.
    """
    async def __aenter__(self):
        """
        Creates an aiohttp session and logs in
        """
        credentials = json.load(open(constants.CREDENTIALS_PATH))
        self.session = aiohttp.ClientSession()
        data = {
            'email': credentials['atlas']['email'],
            'password': credentials['atlas']['password'],
        }
        await self.post('https://authenticate.rubicon.com/api/auth', json=data)
        """
        GET https://monroek12.rubiconatlas.org/c/saml/Webservice.php?Query=Login
        302 Redirect to new location
        Parse URL params for SAMLRequest
        GET https://authenticate.rubicon.com/api/auth/saml?RelayState=&SAMLRequest=
        RelayState: https://monroek12.rubiconatlas.org/Atlas/Authentication/View/Login?AllowLegacyLogin=0
        This gives a SAMLResponse to be posted to another URL (https://monroek12.rubiconatlas.org/c/lib/simplesaml/module.php/saml/sp/saml2-acs.php/rubiconnt-saml)
        That response sets the SimpleSAMLAuthToken cookie
        """
        self.users = await Users.create(self)
        for cookie in self.session.cookie_jar:
            print(cookie.key, cookie.value)

    async def __aexit__(self, *exc):
        """
        Closes aiohttp session
        """
        await self.session.close()
        for cookie in self.session.cookie_jar:
            print(cookie.key, cookie.value)

    async def request(self, method, url, json, params):
        """
        Perform an HTTP request and do some error checking
        """
        logging.debug('HTTP {} {} params={} json={}'.format(method, url,
            params, json))
        async with self.session.request(method, url, params=params, json=json) as resp:
            logging.debug('HTTP RESPONSE {}'.format(resp.status))
            if resp.status != 200:
                logging.error('HTTP {}'.format(resp.status))
                system.exit(1)
            print(resp)
            return resp

    async def post(self, url, json=None, params=None):
        """
        Shortcut for HTTP POST
        """
        return await self.request('POST', url, json=json, params=params)

    async def get(self, url, json=None, params=None):
        """
        Shortcut for HTTP GET
        """
        return await self.request('GET', url, json=json, params=params)
