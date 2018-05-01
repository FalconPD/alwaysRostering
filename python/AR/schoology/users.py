"""Functions relating to users"""

from AR.schoology import roles, utils

add_queue = []
delete_queue = []
chunk_size = 50

async def list():
    """Returns a lists of users one page at a time."""

    async for json_response in utils.list_pages('users'):
        yield json_response['user'] 

async def create_update(school_uid, name_first, name_last, email, role):
    """Creates a user object, adds it to the queue, and if the queue is at the
    chunk_size it sends out a request to add that block of users"""

    user = {
        'school_uid': school_uid,
        'name_first': name_first,
        'name_last': name_last,
        'primary_email': email,
        'role_id': roles.lookup_id(role),
        'synced': 1
    }

    add_queue.append(user)
    if len(add_queue) == chunk_size:
        flush()

async def delete(uid):
    """Deletes users in chunks
    Defaults: do not notify via email, keeps attendance and grade info, and
    set comment to 'automated delete'"""

    delete_queue.append(uid)
    if len(delete_queue) == chunk_size:
        flush()

async def flush():
    """Sends requests for the add/delete queues and clears them"""

    global add_queue, delete_queue

    if len(add_queue) > 0:
        json_data = { 'users': { 'user': add_queue } }
        params = { 'update_existing': 1 }
        await utils.post('users', json=json_data, params=params)
        add_queue = []
    if len(delete_queue) > 0:
        params = {
            'uids': ','.join(map(str, delete_queue)),
            'option_comment': 'automated delete',
            'option_keep_enrollments': '1',
            'email_notification': '0'
        }
        await utils.delete('users', params=params)
        delete_queue = []
