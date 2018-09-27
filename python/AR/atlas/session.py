from AR.atlas import constants
from AR.atlas import Users
import json
import aiohttp
import logging
import pprint
import urllib.parse as urlparse
from bs4 import BeautifulSoup
import sys

pp=pprint.PrettyPrinter(indent=4)

class Session():
    """
    A context manager to handle logging in, loading users, etc.
    """
    async def __aenter__(self):
        """
        Creates an aiohttp session, logs in, gets a list of users
        """
        self.session = aiohttp.ClientSession()
        await self.login()
        self.users = await Users.create(self)
        pp.pprint(self.users.find_by_name("Ryan", "Tolboom"))        

    async def __aexit__(self, *exc):
        """
        Closes aiohttp session
        """
        await self.session.close()
        for cookie in self.session.cookie_jar:
            print(cookie.key, cookie.value)

    async def login(self):
        """
        Logs into Atlas

        1. POST a JSON username and password to
        https://authenticate.rubicon.com/api/auth. The response sets a session
        cookie and a PHPSamlSESSID cookie.

        2. GET https://monroek12.rubiconatlas.org/c/saml/Webservice.php?Query=login
        which returns a 302 redirect with SAMLRequest in a fragment of the URL.

        3. GET https://authenticate.rubicon.com/api/auth/saml with RelayState
        and SAMLRequest as query params gives us a form

        4. Parse the form to get a SAMLResponse to submit.

        5. POST SAMLResponse to action URL of the form. This sets the
        SimpleSAMLAuthToken cookie and returns a redirect.
        """
        credentials = json.load(open(constants.CREDENTIALS_PATH))
        data = {
            'email': credentials['atlas']['email'],
            'password': credentials['atlas']['password'],
        }
        await self.post('https://authenticate.rubicon.com/api/auth', json=data)

        params = { 'Query': 'Login' }
        response = await self.get('https://monroek12.rubiconatlas.org/c/saml/Webservice.php',
            params=params, allow_redirects=False)
        location_url = response.headers.get("Location")
        parsed = urlparse.urlparse(location_url, allow_fragments=False)
        saml_request = urlparse.parse_qs(parsed.query)['SAMLRequest'][0]

        relay_state = 'https://monroek12.rubiconatlas.org/Atlas/Authentication/View/Login?AllowLegacyLogin=0'
        params = {
            'RelayState': relay_state,
            'SAMLRequest': saml_request,
        }
        response = await self.get('https://authenticate.rubicon.com/api/auth/saml', params=params)
        form_html = await response.text()

        soup = BeautifulSoup(form_html, 'html.parser')
        saml_response = soup.find('input', {'name': 'SAMLResponse'})['value']
        relay_state = soup.find('input', { 'name': 'RelayState' })['value']
        action = soup.find('form', {'name': 'hiddenform'})['action']
        data = { 'SAMLResponse': saml_response, 'RelayState': relay_state, }
        await self.post(action, data=data, allow_redirects=False)

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
