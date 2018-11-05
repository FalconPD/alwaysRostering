import logging

class User():
    """
    This class represents the information stored for a user in Atlas
    """
    first_name = None
    last_name = None
    email = None
    attributes = []
    privileges = []

    def __init__(self, atlas_id, first_name, last_name, email, attributes,
        privileges):
        self.atlas_id = atlas_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.attributes = attributes
        self.privileges = privileges

    def save_object(self):
        """
        Returns an Atlas object for this user that can be used to
        create / update their information
        """
        data = {
            'Populate': False,
            'Type': 'Teacher',
            'ID': self.atlas_id, 
            'TeacherLast': self.last_name,
            'TeacherFirst': self.first_name,
            'Email': self.email,
        }
        if 'System Admin' in self.attributes:
            data['TeacherIsAdmin'] = '1'
        if self.atlas_id == '':
            data['SendInvitationEmail'] = '1'
        return data

    def privilege_object(self):
        """
        Returns an Atlas object for this user that can be used to update their
        privileges
        """
        data = {
            'Populate': False,
            'Type': 'Teacher',
            'ID': self.atlas_id, 
        }
        if 'All-level editing privileges' in self.privileges:
            data['SaveTeacherPrivileges'] = '1'
            data['ogPriv'] = 'All'
        return data

    def delete_object(self):
        """
        Returns an Atlas object for this user that can be used to
        delete them
        """
        data = {
            'Populate': False,
            'Type': 'Teacher',
            'ID': self.atlas_id, 
        }
        return data

    def equal(self, user):
        """
        Compare ourself to another User instance and return True if they are
        equal
        """
        logging.debug("Comparing:")
        logging.debug("> Self: {}".format(self))
        logging.debug("> Other: {}".format(user))
        if self.atlas_id != user.atlas_id:
            logging.debug( "> Atlas IDs do not match")
            return False
        if self.first_name != user.first_name:
            logging.debug("> First names do not match")
            return False
        if self.last_name != user.last_name:
            logging.debug("> Last names do not match")
            return False
        if self.email != user.email:
            logging.debug("> Emails do not match")
            return False
        if self.attributes != user.attributes:
            logging.debug("> Attributes do not match")
            return False
        if self.privileges != user.privileges:
            logging.debug("> Privileges do not match")
            return False
        return True

    def __repr__(self):
        return (
            "User "
            "atlas_id={} "
            "first_name={} "
            "last_name={} "
            "email={} "
            "attributes={} "
            "privileges={}"
        ).format(
            self.atlas_id,
            self.first_name,
            self.last_name,
            self.email,
            self.attributes,
            self.privileges
        )
