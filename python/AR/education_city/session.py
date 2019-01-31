import asyncio
import aiohttp
import logging
import sys
import csv

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import AR.credentials as credentials
from AR.education_city.download_mixin import DownloadMixin

class Session(DownloadMixin):
    """
    A context manager to handle logging in
    """
    def __init__(self, school_code, db_file, loop):
        """
        Setup the school code
        """
        self.school_code = school_code
        self.db_file = db_file
        self.loop = loop

    async def __aenter__(self):
        """
        Creates an aiohttp session, logs in, and sets up a database session.
        Education City has a different admin setup for each school so you must
        specify a school code
        """
        self.session = aiohttp.ClientSession()
        await self.login()
        
        self.engine = create_engine(f'sqlite:///{self.db_file}')
        Session = sessionmaker(bind=self.engine)
        self.db_session = Session()
        return self

    async def __aexit__(self, *exc):
        """
        Closes aiohttp session and database session
        """
        await self.session.close()
        self.db_session.commit()

    async def request(self, method, url, data):
        """
        Perform an HTTP request and do some error checking
        """
        logging.debug(f"HTTP {method} {url} data={data}")
        resp = await self.session.request(method, url, data=data)
#            proxy='http://localhost:8888', verify_ssl=False)
        logging.debug('HTTP RESPONSE {}'.format(resp.status))
        if resp.status >= 400:
            logging.error('HTTP {}'.format(resp.status))
            sys.exit(1)
        return resp

    async def post(self, url, data=None):
        """
        Shortcut for HTTP POST
        """
        return await self.request('POST', url, data)

    async def get(self, url):
        """
        Shortcut for HTTP GET
        """
        return await self.request('GET', url)

    async def login(self):
        """
        Log in to the admin page for a particular school
        """
        school_credentials = credentials.education_city[self.school_code]
        data = {
            'username': school_credentials['username'],
            'password': school_credentials['password'],
        }
        await self.post('https://ec2.educationcity.com/home/doProductLogin',
            data=data)
