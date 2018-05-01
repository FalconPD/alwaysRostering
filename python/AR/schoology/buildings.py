"""Functions relating to creating / loading / listing buildings"""
from AR.schoology import utils
from AR.schoology import schools

buildings = None

async def load():
    """This wrapper function allows us to reload the buildings after we
    create/update them"""
    global buildings

    buildings = await list()

def lookup_id(building_code):
    """Check our internal list of buildings to look up the ID"""
    for building in buildings['building']:
        if building['building_code'] == building_code:
            return building['id']
    return None

async def list():
    """Downloads all of the buildings from Schoology"""

    resp = await utils.get('schools/' + schools.school_id + '/buildings')
    return await resp.json()

async def create_update(title, building_code, address1='', address2='',
    city='Monroe Township', state='NJ', postal_code='08831', country='USA',
    website='', phone='', fax='', picture_url=''):
    """Looks up a building, if it doesn't exist creates it, otherwise updates
    its information. Has some built-in defaults for Monroe"""

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

    building_id = lookup_id(building_code)
    if (building_id): # update
        await utils.put('schools/' + building_id, json=json_data)
    else: # create
        await utils.post('schools/' + school_id + '/buildings', json=json_data)
