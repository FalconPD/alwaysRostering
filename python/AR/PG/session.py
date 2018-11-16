import time
import aiohttp
import json
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

from AR.atlas import constants
from AR.util.token_bucket import TokenBucket
from AR.PG.http_mixin import HTTPMixin
from AR.PG.users_mixin import UsersMixin

class Session(HTTPMixin, UsersMixin):
    """
    A context manager to handle logging in and loading users
    """
    session = None # our aiohttp session

    async def __aenter__(self):
        """
        Creates an aiohttp session, logs in
        """
        self.token_bucket = TokenBucket(100, 50)
        cookies = await self.login()
        self.session = aiohttp.ClientSession(cookies=cookies)
        await self.load_users()
        return self

    async def __aexit__(self, *exc):
        """
        Closes aiohttp session, writes map
        """
        await self.session.close()

    async def login(self):
        """
        Logs into Frontline PG using Selenium. This is required as the login
        routine is *WACKY* (AngularJS models refreshing pages, etc.). It
        returns a set of cookies that can be used by aiohttp to access
        MyLearningPlan
        """
        # Setup our headless browser
        opts = Options()
        opts.set_headless()
        assert opts.headless
        with Firefox(options=opts) as browser:
            # Some things take a while to settle (redirects, JS redirects, etc.)
            browser.implicitly_wait(10)

            # Submit credentials on the login page
            browser.get('https://mylearningplan.com')
            credentials = json.load(open(constants.CREDENTIALS_PATH))
            browser.find_element_by_id('Username').send_keys(credentials['pg']['username'])
            browser.find_element_by_id('Password').send_keys(credentials['pg']['password'])
            browser.find_element_by_id('qa-button-login').click()

            # Redirect to MyLearningPlan so we can get the cookies used for it
            browser.get('https://www.mylearningplan.com/DistrictAdmin/UserList.asp')
            aiohttp_cookies = {}
            for cookie in browser.get_cookies():
                aiohttp_cookies[cookie['name']] = cookie['value']
            return aiohttp_cookies
