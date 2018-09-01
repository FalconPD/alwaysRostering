from AR.schoology.lookup import Lookup

class Buildings(Lookup):
    """
    Class for handling Buildings
    """
    heading = 'building'
    lookup_by = 'building_code'

    @classmethod
    async def create(cls, session):
        """
        Custom create function needed to set the endpoint as it requires
        a lookup of school_id
        """

        self = cls()
        self.session = session
        self.endpoint = 'schools/' + session.Schools.school_id + '/buildings'
        await self.load()
        return self

    async def __aenter__(self):
        """
        After adding buildings, it's important that you reload them for the
        lookup table. This context manager simplifies that.
        """
        return self

    async def __aexit__(self, *exc):
        await self.load()

    async def add_update(self, title, building_code, address1='', address2='',
        city='Monroe Township', state='NJ', postal_code='08831', country='USA',
        website='', phone='', fax='', picture_url=''):
        """
        Looks up a building, if it doesn't exist creates it, otherwise updates
        its information. Has some built-in defaults for Monroe
        """
        json_data = {
            'title': title,
            'building_code': building_code,
            'address1': address1,
            'address2': address2,
            'city': city,
            'state': state,
            'postal_code': postal_code,
            'country': country,
            'website': website,
            'phone': phone,
            'fax': fax,
            'picture_url': picture_url
        }

        building_id = self.lookup_id(building_code)
        school_id = self.session.Schools.school_id
        if (building_id): # update
            await self.session.put('schools/' + building_id, json=json_data)
        else: # create
            await self.session.post('schools/' + school_id + '/buildings', json=json_data)
