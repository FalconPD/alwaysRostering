from bs4 import BeautifulSoup

class UsersMixin():
    """
    This mixin provides routines for dealing with PG users
    """
    async def parse_user_profile(self, url):
        """
        Loads a user profile page, parses it and returns a user object
        """
        resp = await self.get(url)
        soup = BeautifulSoup(await resp.text(), 'html.parser')
        first_name = soup.find('input', id='VAR_FIRSTNAME')['value']
        print(first_name)
        
    async def load_users(self):
        """
        Gets a list of all users on PG and stores it in the users variable
        """
        resp = await self.get('https://www.mylearningplan.com/DistrictAdmin/UserList.asp?V=ALL')
        soup = BeautifulSoup(await resp.text(), 'html.parser')
        for link in soup('a'):
            href = link.get('href')
            if href.startswith('/Forms.asp'):
                await self.parse_user_profile('https://www.mylearningplan.com' + href)
