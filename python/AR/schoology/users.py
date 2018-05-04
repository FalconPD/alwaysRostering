from AR.schoology import constants

class Users():
    """Handles our user operations"""

    @classmethod
    async def create(cls, session):
        """Creates a User object linked to a session"""

        self = cls()
        self.session = session
        return self

    async def __aenter__(self):
        """Creates our queues"""

        self.add_queue = []
        self.del_queue = []
        return self

    async def __aexit__(self, *exc):
        """Flushes anything left over"""

        await self.flush()

    async def list(self):
        """Returns a lists of users one page at a time."""

        async for json_response in self.session.list_pages('users'):
            yield json_response['user'] 

    async def add_update(self, school_uid, name_first, name_last, email, role):
        """Makes a user object, adds it to the queue, and if the queue is at
        the chunk_size it sends out a request to add that block of users"""

        user = {
            'school_uid': school_uid,
            'name_first': name_first,
            'name_last': name_last,
            'primary_email': email,
            'role_id': self.session.Roles.lookup_id(role),
            'synced': 1
        }

        self.add_queue.append(user)
        if len(self.add_queue) == constants.CHUNK_SIZE:
            await self.flush()

    async def delete(self, uid):
        """Deletes users in chunks
        Defaults: do not notify via email, keeps attendance and grade info, and
        set comment to 'automated delete'"""

        self.del_queue.append(uid)
        if len(self.del_queue) == constants.CHUNK_SIZE:
            await self.flush()

    async def flush(self):
        """Sends requests for the add/delete queues and clears them"""

        if len(self.add_queue) > 0:
            json_data = { 'users': { 'user': self.add_queue } }
            params = { 'update_existing': 1 }
            await self.session.post('users', json=json_data, params=params)
            self.add_queue = []
        if len(self.del_queue) > 0:
            params = {
                'uids': ','.join(map(str, self.del_queue)),
                'option_comment': 'automated delete',
                'option_keep_enrollments': '1',
                'email_notification': '0'
            }
            await self.session.delete('users', params=params)
            self.del_queue = []
