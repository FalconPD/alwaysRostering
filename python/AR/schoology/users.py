from AR.schoology.queue import AddDel

class Users(AddDel):
    """Handles our user operations"""

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

        await self.adds.add(user)

    async def delete(self, uid):
        """
        Deletes users
        Defaults: do not notify via email, keeps attendance and grade info, and
        set comment to 'automated delete'
        """
        await self.dels.add(uid)

    async def send_adds(self, adds):
        """
        Sends request to add users. Specifies to update existing users and
        merge existing accounts with our domain if found.
        """
        json_data = { 'users': { 'user': adds } }
        params = { 'update_existing': 1,
                   'email_conflict_resolution': 2 }
        await self.session.post('users', json=json_data, params=params)

    async def send_dels(self, dels):
        """
        Sends a request to delete users
        """
        params = {
            'uids': ','.join(map(str, dels)),
            'option_comment': 'automated delete',
            'option_keep_enrollments': '1',
            'email_notification': '0'
        }
        await self.session.delete('users', params=params)
