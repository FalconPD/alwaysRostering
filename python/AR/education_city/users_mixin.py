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

    async def _validate_user_list(self, users, user_type):
        """
        Adds users through the user_management/validateUserList interface
        NOTE: This is different than bulk_user_management and seems to just be
        used for teachers. It uses form data instead of json.
        """
        data = {
            'user_csv_data': "",
            'user_type_id': user_type,
            'save': 1,
        }
        for user in users:
            data['user_csv_data'] += (f"{user['title']},{user['first_name']},"
                f"{user['last_name']},{user['username']},{user['password']},"
                f"{user['email']}\n")
        resp = await self.post(
            'https://ec2.educationcity.com/user_management/validateUserList',
            data=data)
        print(await resp.text())

    async def addmod_teachers(self, teachers):
        """
        Adds or modifies teachers
        """
        await self._validate_user_list(teachers, constants.USERTYPE_TEACHER)

    async def _delete(self, users, user_type):
        """
        Deletes a list of users. 
        """
        json = {
            'data': {
                'ids': '',
                'type': user_type,
            },
            'method': 'delete',
        }
        for user in users:
            json['data']['ids'] += f"{user['id']}-"
        await self.post('https://ec2.educationcity.com/api/user/', json=json)

    async def del_teachers(self, teachers):
        """
        Deletes a list of teachers
        """
        await self._delete(teachers, constants.USERTYPE_TEACHER)

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
            if user_defined_id != None:
                self.users[user_type][user_defined_id] = user_info
            else:
                username = user_info['username']
                self.users[user_type][username] = user_info
            
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
