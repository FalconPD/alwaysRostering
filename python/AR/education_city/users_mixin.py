from AR.education_city import constants

import pprint
import asyncio
import json

class UsersMixin():
    """
    Handles users in Education City
    """
    async def _bulk_user_management(self, users, user_type, commit=False,
        skip_warnings=False):
        """
        Uses the bulk_user_management API in Education City
        """
        json = {
            'commit': commit,
            'data': [],
            'skip_warnings': skip_warnings,
            'user_type': user_type,
        }
        for user in users:
            json['data'].append(user)
        resp = await self.post(
            'https://ec2.educationcity.com/api/bulk_user_management',
            json=json)
        print(await resp.json())

    async def addmod_students(self, students):
        """
        Adds or modifies students
        """
        await self._bulk_user_management(students,
            constants.USERTYPE_STUDENT, commit=True)

    async def _get_user_info(self, user_type):
        """
        Downloads JSON information for a user type and sets up a dict by UniqueID
        """
        self.users[user_type] = {}
        resp = await self.get(
            f'https://ec2.educationcity.com/api/user/type/{user_type}')
        json = await resp.json()
        for key, user_info in json.items():
            user_defined_id = user_info['user_defined_id']
            self.users[user_type][user_defined_id] = user_info
            
    async def download(self):
        """
        Downloads JSON information about all user types
        """
        self.users={}
        tasks = []
        for user_type in constants.USERTYPES:
            tasks.append(self.loop.create_task(self._get_user_info(user_type)))
        await asyncio.gather(*tasks)

    async def save(self, output_file):
        """
        Saves JSON user information to a file
        """
        with open(output_file, 'w') as f:
            json.dump(self.users, f, sort_keys=True, indent=4)
