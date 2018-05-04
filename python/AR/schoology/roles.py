from AR.schoology.lookup import Lookup
import logging

class Roles(Lookup):
    """Class for handling roles"""

    endpoint = 'roles'
    heading = 'role'
    lookup_by =  'title'
