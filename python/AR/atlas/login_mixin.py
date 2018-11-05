import json
import re
import urllib.parse as urlparse
from bs4 import BeautifulSoup

from AR.atlas import constants

class LoginMixin():
    """
    This mixin contains the function for logging into Atlas
    """    
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
        response = await self.get(constants.BASE_URL + 'c/saml/Webservice.php',
            params=params, allow_redirects=False)
        location_url = response.headers.get("Location")
        parsed = urlparse.urlparse(location_url, allow_fragments=False)
        saml_request = urlparse.parse_qs(parsed.query)['SAMLRequest'][0]

        relay_state = constants.BASE_URL + 'Atlas/Authentication/View/Login?AllowLegacyLogin=0'
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
