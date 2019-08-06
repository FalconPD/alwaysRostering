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
        """
        Check our internal data to look up the ID. This returns the ID or None
        """
        for datum in self.data:
            if datum[self.lookup_by] == comparison:
                return datum['id']
        logging.warning('Unable to lookup {} (endpoint={})'.format(
            comparison, self.endpoint))
        return None

    def lookup(self, comparison):
        """
        Check our internal data to to find the one that matches. This returns
        the data or none
        """
        for datum in self.data:
            if datum[self.lookup_by] == comparison:
                return datum
        logging.warning('Unable to lookup {} (endpoint={})'.format(
            comparison, self.endpoint))
        return None

    async def list(self):
        """Downloads the data from Schoology"""

        resp = await self.session.get(self.endpoint)
        json_response = await resp.json()
        # Grading periods returns {'total': 0} if there are no grading periods
        if 'total' in json_response and json_response['total'] == 0:
            logging.warning(f"No {self.heading}s set up in Schoology")
            return []            
        return json_response[self.heading]
