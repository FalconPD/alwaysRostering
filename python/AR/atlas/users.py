import csv
from io import StringIO
import pprint

pp = pprint.PrettyPrinter(indent=4)
 
class Users():
    """
    Handles users operations
    """
    @classmethod
    async def create(cls, session):
        """
        Creates an object linked to a session
        Need a factory function due to async
        """
        self = cls()
        self.session = session
        await self.refresh()
        return self

    async def refresh(self):
        """
        Gets a list of the users from Atlas from a CSV export
        """
        resp = await self.session.get( 'https://monroek12.rubiconatlas.org/' +
            'Atlas/Admin/View/TeachersExport?CSVDoc=1')
        buff = StringIO(await resp.text())
        users = []
        for line in csv.DictReader(buff):
            users.append(line)
        self.users = users
        pp.pprint(self.users)

    def find_by_email(self, email):
        """
        Case insensitive email search that returns first match
        """
        for user in self.users:
            if user['Email'].lower() == email.lower():
                return user
        return None

    def find_by_name(self, first_name, last_name):
        """
        Case insensitive first and last name search that returns first match
        """
        for user in self.users:
            if user['Last Name'].lower() == last_name.lower() and user['First Name'].lower() == first_name.lower():
                return user
        return None
