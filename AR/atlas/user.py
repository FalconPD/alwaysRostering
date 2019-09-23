import logging

class User():
    """
    This class represents the information stored for a user in Atlas
    """
    first_name = None
    last_name = None
    emails = []
    attributes = []
    privileges = []

    def __init__(self, atlas_id, first_name, last_name, emails, attributes,
        privileges):
        self.atlas_id = atlas_id
        self.first_name = first_name
        self.last_name = last_name
        self.emails = emails
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
            'Email': self.emails[0],
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

    def __repr__(self):
        return (f"User atlas_id={self.atlas_id} first_name={self.first_name} "
                f"last_name={self.last_name} email={self.emails} "
                f"attributes={self.attributes} privileges={self.privileges}")
