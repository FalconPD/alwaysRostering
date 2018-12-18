from bs4 import BeautifulSoup
from AR.PG.user import User
import asyncio
import logging
import sys
import re
import json

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
        Gets all ACTIVE users on PG and puts them in a dict by payroll_id
        A user MUST have a valid and unique payroll_id in PG for this to work
        """
        resp = await self.get('https://www.mylearningplan.com/DistrictAdmin/UserList.asp?V=A')
        soup = BeautifulSoup(await resp.text(), 'html.parser')
        tasks = []
        for link in soup('a'):
            href = link.get('href')
            if href.startswith('/Forms.asp?F=INT_USERID&M=E&I='):
                tasks.append(self.parse_user_profile('https://www.mylearningplan.com' + href))
        payroll_id_regex = re.compile('\d{6}')
        users = {}
        for user in await asyncio.gather(*tasks):
            if (payroll_id_regex.match(user.payroll_id) and
                user.payroll_id not in users):
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
        h1 = soup.find('h1')
        if h1 == None or list(h1.strings)[0] != 'Confirmation':
            logging.error("Error(s) while saving user {}:".format(user))
            for error in soup.find('ul', class_='alert-error-list').strings:
                logging.error("{}".format(error))
            sys.exit(1)

    def save_user_snapshot(self, filename):
        """
        Saves our list of users in a JSON file
        """
        with open(filename, 'w') as out:
            dict_users = {}
            for payroll_id, user in self.users.items():
                dict_users[payroll_id] = user.to_dict() # json serializable
            json.dump(dict_users, out, sort_keys=True, indent=4)
