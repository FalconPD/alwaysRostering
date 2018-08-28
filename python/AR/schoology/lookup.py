import logging

class Lookup():
    """General class for our lookup table classes"""

    @classmethod
    async def create(cls, session):
        """Factory function for this class. Needed due to async"""

        self = cls()
        self.session = session
        await self.load()
        return self

    async def load(self):
        """Load the data from Schoology"""

        self.data = await self.list()

    def lookup_id(self, comparison):
        """Check our internal data to look up the ID"""

        for datum in self.data:
            if datum[self.lookup_by] == comparison:
                return datum['id']
        logging.warning('Unable to lookup {} (endpoint={})'.format(
            comparison, self.endpoint))
        return None

    async def list(self):
        """Downloads the data from Schoology"""

        resp = await self.session.get(self.endpoint)
        json_response = await resp.json()
        return json_response[self.heading]
