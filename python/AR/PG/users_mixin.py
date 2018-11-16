from bs4 import BeautifulSoup
from AR.PG.user import User
import asyncio

class UsersMixin():
    """
    This mixin provides routines for dealing with PG users
    """
    async def parse_user_profile(self, url):
        """
        Loads a user profile page, parses it and returns a user object
        """
        resp = await self.get(url)
        user = User(await resp.text())
        return user
        
    async def load_users(self):
        """
        Gets a list of all users on PG and stores it in the users variable
        """
        resp = await self.get('https://www.mylearningplan.com/DistrictAdmin/UserList.asp?V=ALL')
        soup = BeautifulSoup(await resp.text(), 'html.parser')
        tasks = []
        for link in soup('a'):
            href = link.get('href')
            if href.startswith('/Forms.asp?F=INT_USERID&M=E&I='):
                tasks.append(self.parse_user_profile('https://www.mylearningplan.com' + href))
        users = []
        for user in await asyncio.gather(*tasks):
            users.append(user)
        self.users = users

    def find_user(self, first, last):
        """
        Performs a CASE INSENSITIVE search for a user based on first and last name
        """
        for user in self.users:
            if first.upper() == user.first_name.upper() and last.upper() == user.last_name.upper():
                return user
        return None
