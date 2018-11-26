import time
import aiohttp
import json
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

from AR.util.token_bucket import TokenBucket
from AR.PG import constants
from AR.PG.http_mixin import HTTPMixin
from AR.PG.users_mixin import UsersMixin
from AR.PG.user import User

class Session(HTTPMixin, UsersMixin):
    """
    A context manager to handle logging in and loading users
    """
    session = None # our aiohttp session

    def __init__(self, user_file):
        self.user_file = user_file

    async def __aenter__(self):
        """
        Logs in with selenium, creates and aiohttp session with the cookies
        from selenium, loads users from a file or PG
        """
        self.token_bucket = TokenBucket(constants.MAX_TOKENS,
            constants.TOKEN_RATE) 
        cookies = await self.login()
        self.session = aiohttp.ClientSession(cookies=cookies)
        if self.user_file != None:
            try:
                self.users = {}
                for payroll_id, user_dict in json.load(open(self.user_file)).items():
                    self.users[payroll_id] = User(dict_=user_dict)
            except FileNotFoundError:
                self.users = await self.load_users()
        return self

    async def __aexit__(self, *exc):
        """
        Closes aiohttp session, writes PG users if requested
        """
        await self.session.close()
        if self.user_file != None:
            with open(self.user_file, 'w') as out:
                dict_users = {}
                for payroll_id, user in self.users.items():
                    dict_users[payroll_id] = user.__dict__
                json.dump(dict_users, out, sort_keys=True, indent=4) 

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
            browser.implicitly_wait(constants.SELENIUM_TIMEOUT)

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
