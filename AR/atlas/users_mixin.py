from bs4 import BeautifulSoup
import re
import logging
import asyncio
import json

from AR.atlas import constants
from AR.atlas.user import User

class UsersMixin():
    """
    Mixin to provide users functions
    """
    async def parse_user_page(self, url):
        """
        GETs and parses a users page, returning a list of User instances
        """
        resp = await self.get(url)
        soup = BeautifulSoup(await resp.text(), 'html.parser')
        rows = soup('tr', {'class': 'Teacher'})
        for row in rows[1:]: # Skip the first row
            atlas_id = re.search('Teacher_row_(.*)', row['id']).group(1)
            td = list(row('td'))
            name = td[0].string.split(', ')
            last_name = name[0]
            first_name = name[1]
            emails = list(td[1].stripped_strings)
            attributes = [ i for i in td[2].stripped_strings ]
            privileges = [ i for i in td[3].stripped_strings ]
            self.users[atlas_id] = User(atlas_id, first_name, last_name, emails,
                attributes, privileges)

    async def load_users(self):
        """
        Loads / parses the users pages on Atlas to create a users list
        """
        # see how many pages there are
        resp = await self.get(constants.BASE_URL + 'Atlas/Admin/View/Teachers')
        soup = BeautifulSoup(await resp.text(), 'html.parser')
        span = soup.find('span', {'class': 'UIPagingShowing'})
        max_pages = int(re.search('\(Page 1 of (\d+), Records.*',
            span.contents[0]).group(1))

        # Load all the pages asynchronously
        logging.debug(f"Loading {max_pages} pages of users")
        tasks = []
        for page in range(1, max_pages + 1):
            tasks.append(self.parse_user_page(constants.BASE_URL +
                f'Atlas/Admin/View/Teachers?Page={page}'))
        await asyncio.gather(*tasks)

    async def action(self, action, method, atlas_object):
        """
        Performs an Atlas controller action with the given object. Actions are
        form style POST requests with URL encoded JSON. Returns the response.
        """
        json_data = {
            action: {
                "Object": atlas_object,
                "Method": method,
                "Parameters":{},
            }
        }
        form_data = {'Actions': json.dumps(json_data)}
        resp = await self.post(constants.BASE_URL + 'Atlas/Controller',
                               data=form_data)
        response_json = await resp.json(content_type=None)
        logging.debug(f"Action Response: {response_json}")
        return response_json

    async def save_user(self, user):
        """
        Save a User object in Atlas. The POST request is URL encoded JSON.
        Returns the Atlas ID of the object.
        """
        response_json = await self.action("Save", "AsyncSave",
            user.save_object())
        message = response_json['Save']
        if 'ID' not in message:
            logging.error(f"Unable to save user {user}")
            return None
        if message['ID'] == 'Invalid Email Address':
            logging.error(f"Unable to save user {user}: Invalid Email Address")
            return None
        return str(message['ID'])

    async def delete_user(self, user):
        """
        Deletes a user from Atlas and the users dict
        """
        response_json = await self.action("Delete", "AsyncDelete",
            user.delete_object())
        message = response_json['Delete']
        if 'Result' not in message:
            logging.error(f"Unable to delete user {user} (no result)")
            return
        else:
            if message['Result'] != 'OK':
                logging.error(f"Unable to delete user {user}")
            return
        atlas_id = user.atlas_id
        del(self.users[atlas_id])

    async def update_privilege(self, user):
        """
        Updates a user's privileges in Atlas.
        """
        response_json = await self.action("Save", "AsyncSave",
            user.privilege_object())
        message = response_json['Save']
        if 'ID' not in message:
            logging.error(f"Unable to update privileges for user {user}")
            return None
        return message['ID']

    async def update_user(self, user):
        """
        Updates / creates a user object on Atlas, updates the users
        dict, and sets the pivileges if necessary. Returns the user
        """
        atlas_id = await self.save_user(user)
        if user.atlas_id == '':
            user.atlas_id = atlas_id
            self.users[atlas_id] = user
        if len(user.privileges) != 0:
            await self.update_privilege(user)
        return user

    def email_to_user(self):
        """
        Creates a dictionary where the keys are uppercase emails and the values
        are User objects that have that email.
        """
        email_to_user_dict = {}
        for atlas_id, user in self.users.items():
            for email in user.emails:
                email_to_user_dict[email.upper()] = user
        return email_to_user_dict

    def find_user_by_name(self, first, last):
        """
        Looks up a user by their first and last name. The search is case
        insensitive and returns None on failure.
        """
        upper_first = first.upper()
        upper_last = last.upper()
        for atlas_id, user in self.users.items():
            if (upper_first == user.first_name.upper() and
                upper_last == user.last_name.upper()):
                return user
        return None
