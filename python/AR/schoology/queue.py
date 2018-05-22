from AR.schoology import constants

class Queue():
    """Creates a list of objects that are pushed to a send function once the
    list reaches CHUNK_SIZE"""

    def __init__(self, send_func):
        self.send = send_func
        self.data = []

    async def add(self, obj):
        """Adds an object to the queue and flushes the queue if it is at
        CHUNK_SIZE"""

        self.data.append(obj)
        if len(self.data) == constants.CHUNK_SIZE:
            await self.flush()

    async def flush(self):
        """Triggers the send function and clears the queue"""

        if len(self.data) > 0:
            # Copy because have to clear self.data before giving away control
            data = self.data 
            self.data = []
            await self.send(data)

class AddDel():
    """This is a generic template for an object that uses adds and dels
    queues"""

    @classmethod
    async def create(cls, session):
        """Creates an object linked to a session"""

        self = cls()
        self.session = session
        return self

    async def __aenter__(self):
        """Creates our queues"""

        self.adds = Queue(self.send_adds)
        self.dels = Queue(self.send_dels)
        return self

    async def __aexit__(self, *exc):
        """Flushes anything left over"""

        await self.adds.flush()
        await self.dels.flush()

