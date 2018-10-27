import csv
from io import StringIO
import json
import logging
from bs4 import BeautifulSoup
import re

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
        resp = await self.session.get('https://monroek12.rubiconatlas.org/' +
            'Atlas/Admin/View/TeachersExport?CSVDoc=1')
        buff = StringIO(await resp.text(encoding='utf-8-sig'))
        users = []
        for line in csv.DictReader(buff):
            users.append(line)
        self.users = users

    async def test(self):
        # Load the users page to see how many pages there are
        resp = await self.session.get('https://monroek12.rubiconatlas.org/' +
            'Atlas/Admin/View/Teachers')
        soup = BeautifulSoup(await resp.text(), 'html.parser')
        span = soup.find('span', {'class': 'UIPagingShowing'})
        text = span.contents[0]
        regex_result = re.search('\(Page 1 of (\d+), Records.*', text)
        max_pages = int(regex_result.group(1))
        print(max_pages)
        for row in soup.find_all('tr', {'class': 'Teacher'}):
            print(row.id)

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

    async def add_user(self, first_name, last_name, email, admin=False):
        """
        Adds a user to Atlas. The POST request is URL encoded JSON
        """
        json_data = {
            "Save": {
                "Object": {
                    "Populate": False,
                    "Type": "Teacher",
                    "ID": "",
                    "WebPass": "",
                    "HasCustomizedMyAtlas": "",
                    "EmailAlert": "1",
                    "ExemplarTeachNoCourseCertified": "",
                    "ExemplarUnitSubmitted": "",
                    "NumberOfExemplarVisits": "",
                    "PasswordEncrypted": "",
                    "PasswordRequested": "",
                    "LastExemplarVisited": "",
                    "HarvestEmailSent": "",
                    "LastSiteNoticeID": "",
                    "AcceptedExemplarAgreement": "",
                    "PropertiesXML": "",
                    "ReceivedAtlasUpdate": "",
                    "TeacherLast": last_name,
                    "TeacherFirst": first_name,
                    "Email": email,
                    "TeacherIsCoreTeam": "",
                    "TeacherWidgetConfigurationGroupID": "",
                    "TeacherIsAdmin": "1" if admin else "",
                    "WillSendWelcomeEmail": "",
                    "SchoolMessaging": "",
                    "SendInvitationEmail": ""
                },
                "Method": "AsyncSave",
                "Parameters":{}
            }
        }
        form_data = {'Actions': json.dumps(json_data)}
        resp = await self.session.post('https://monroek12.rubiconatlas.org/Atlas/Controller', data=form_data)
        response_json = await resp.json(content_type=None)
        message = response_json['Save']
        if 'ID' not in message:
            logging.error("Unable to add {} {} {}: {}".format(first_name, last_name, email, message))
