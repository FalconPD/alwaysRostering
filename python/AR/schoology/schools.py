from AR.schoology.lookup import Lookup 

class Schools(Lookup):
    """Class for handling Schools. Doesn't actually do any lookups, just sets
    school_id"""

    endpoint = 'schools'
    heading = 'school'

    async def load(self):
        """Loads the school_id"""

        schools = await self.list()
        self.school_id = schools[0]['id']
