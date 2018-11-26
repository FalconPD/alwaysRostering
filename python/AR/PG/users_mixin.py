from bs4 import BeautifulSoup
from AR.PG.user import User
import asyncio
import logging
import sys
import re

class UsersMixin():
    """
    This mixin provides routines for dealing with PG users
    """
    async def parse_user_profile(self, url):
        """
        Loads a user profile page, parses it and returns a user object
        """
        resp = await self.get(url)
        html = await resp.text()
        user = User(html=html)
        return user
        
    async def load_users(self):
        """
        Gets all users on PG and puts them in a dict by payroll_id
        A user MUST have a valid and unique payroll_id in PG for this to work
        """
        resp = await self.get('https://www.mylearningplan.com/DistrictAdmin/UserList.asp?V=ALL')
        soup = BeautifulSoup(await resp.text(), 'html.parser')
        tasks = []
        for link in soup('a'):
            href = link.get('href')
            if href.startswith('/Forms.asp?F=INT_USERID&M=E&I='):
                tasks.append(self.parse_user_profile('https://www.mylearningplan.com' + href))
        payroll_id_regex = re.compile('\d{6}')
        users = {}
        for user in await asyncio.gather(*tasks):
            if payroll_id_regex.match(user.payroll_id):
                users[user.payroll_id] = user
            else:
                logging.warning("Invalid payroll_id {}".format(user))
        return users

    async def save_user(self, user):
        """
        Saves a user object on PG
        """
        resp = await self.post('https://www.mylearningplan.com/Forms.asp',
            data=user.data())
        soup = BeautifulSoup(await resp.text(), 'html.parser')
        if list(soup.find('h1').strings)[0] != 'Confirmation':
            logging.error("Error while saving user {}")
            sys.exit(1)
