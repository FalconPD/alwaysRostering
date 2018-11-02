import csv
import json
import logging
from bs4 import BeautifulSoup
import re
from AR.atlas import constants
import asyncio
from AR.atlas.id_map import ID_Map
from AR.atlas.user import User

class Users():
    """
    Handles users operations
    """
    users = {}
    session = None
    id_map = None

    @classmethod
    async def create(cls, session, map_file):
        """
        Creates an object linked to a session
        Need a factory function due to async
        """
        self = cls()
        self.session = session
        await self.load()
        self.id_map = ID_Map(map_file)
        return self

    async def parse_page(self, url):
        """
        GETs and parses a users page, returning a list of User instances
        """
        resp = await self.session.get(url)
        soup = BeautifulSoup(await resp.text(), 'html.parser')
        rows = soup('tr', {'class': 'Teacher'})
        for row in rows[1:]: # Skip the first row
            atlas_id = re.search('Teacher_row_(.*)', row['id']).group(1)
            td = list(row('td'))
            name = td[0].string.split(', ')
            last_name = name[0]
            first_name = name[1]
            emails = list(td[1].stripped_strings)
            email = emails[0] # for now we only deal with the first email
            attributes = [ i for i in td[2].stripped_strings ]
            privileges = [ i for i in td[3].stripped_strings ]
            self.users[atlas_id] = User(atlas_id, first_name, last_name, email,
                attributes, privileges)
       
    async def load(self):
        """
        Loads / parses the users pages on Atlas to create a users list
        """
        # see how many pages there are
        resp = await self.session.get(constants.BASE_URL +
            'Atlas/Admin/View/Teachers')
        soup = BeautifulSoup(await resp.text(), 'html.parser')
        span = soup.find('span', {'class': 'UIPagingShowing'})
        max_pages = int(re.search('\(Page 1 of (\d+), Records.*',
            span.contents[0]).group(1))

        # Load all the pages asynchronously
        logging.debug("Loading {} pages of users".format(max_pages))
        tasks = []
        for page in range(1, max_pages + 1):
            tasks.append(self.parse_page(constants.BASE_URL + 
                'Atlas/Admin/View/Teachers?Page={}'.format(page)))
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
        resp = await self.session.post(constants.BASE_URL +
            'Atlas/Controller', data=form_data)
        response_json = await resp.json(content_type=None)
        logging.debug("Action Response: {}".format(response_json))
        return response_json

    async def save(self, user):
        """
        Save a User object in Atlas. The POST request is URL encoded JSON.
        Returns the Atlas ID of the object.
        """
        response_json = await self.action("Save", "AsyncSave",
            user.save_object())
        message = response_json['Save']
        if 'ID' not in message:
            logging.error("Unable to save user: {}".format(user))
            return None
        if message['ID'] == 'Invalid Email Address':
            logging.error("Unable to save user: Invalid Email Address")
            return None 
        return str(message['ID'])

    async def delete(self, user):
        """
        Deletes a user from Atlas, the id_map, and the users dict
        """
        response_json = await self.action("Delete", "AsyncDelete",
            user.delete_object())
        message = response_json['Delete']
        if 'Result' not in message:
            logging.error("Unable to delete user (no result)".format(user))
            return
        else:
            if message['Result'] != 'OK':
                logging.error("Unable to delete user".format(user))
            return
        atlas_id = user.atlas_id
        self.id_map.del_by_atlas(atlas_id)
        del(self.users[atlas_id])

    async def update_privilege(self, user):
        """
        Updates a user's privileges in Atlas.
        """
        response_json = await self.action("Save", "AsyncSave",
            user.privilege_object())
        message = response_json['Save']
        if 'ID' not in message:
            logging.error("Unable to update privileges for user {}".format(user))
            return None
        return message['ID']

    async def update(self, user, genesis_id):
        """
        Updates / creates a user object on Atlas, changes the id_map as
        necessary, updates the users dict, and sets the pivileges if
        necessary. Returns the atlas_id
        """
        atlas_id = await self.save(user)
        if user.atlas_id == '':
            user.atlas_id = atlas_id
            self.users[atlas_id] = user
            self.id_map.add(genesis_id, atlas_id)
        if len(user.privileges) != 0:
            await self.update_privilege(user)
        return atlas_id
