from AR.schoology.lookup import Lookup

class Roles(Lookup):
    """
    Class for handling roles
    """
    endpoint = 'roles'
    heading = 'role'
    lookup_by =  'title'
