from bs4 import BeautifulSoup

class User():
    """
    A representation of a Professional Growth user
    """
    def _input_to_string(self, soup, id):
        """
        Returns the value of an input as a string
        """
        return soup.find('input', id=id)['value']

    def _checkboxes_to_list(self, soup, for_attr):
        """
        Creates a list of key / value pairs for checkbox groups
        """
        our_list = []
        for label in soup('label', attrs={'for': for_attr,
            'class': 'iform-label_checkbox'}):
            our_input = label.find('input')
            if our_input.has_attr('checked'):
                name = list(label.strings)[0]
                our_list.append({our_input['value']: name})
        return our_list

    def _radio_to_bool(self, soup, base_id):
        """
        Returns a boolean value from a radio button. Checks the "Yes" button
        """
        return soup.find('input', id=base_id+'_Yes').has_attr('checked')

    def __init__(self, html):
        """
        Parses the profile page html and constructs a user object
        """
        soup = BeautifulSoup(html, 'html.parser')
        self.pg_id = soup.find('input', attrs={'name': 'I'})['value']
        self.first_name = self._input_to_string(soup, 'VAR_FIRSTNAME')
        self.last_name = self._input_to_string(soup, 'VAR_LASTNAME')
        self.email = self._input_to_string(soup, 'VAR_EMAIL')
        self.instructor = self._radio_to_bool(soup, 'BIT_ISINSTRUCTOR')
        self.admin = self._radio_to_bool(soup, 'BIT_ISDISTRICTADMIN')
        self.active = self._radio_to_bool(soup, 'BIT_ACTIVE')
        self.catalogs = self._checkboxes_to_list(soup, 'INT_PROGRAMADMINID')
        self.certificate_holder = self._radio_to_bool(soup, 'BIT_ISINSTRUCTIONAL')
        self.ssn = self._input_to_string(soup, 'ENC_SID')
        self.certificate_id = self._input_to_string(soup, 'VAR_CERTIFICATEID')
        self.certificate_expiration = self._input_to_string(soup, 'DT_CERTIFICATEEXPIRATIONDATE')
        self.dob = self._input_to_string(soup, 'DT_DATEOFBIRTH')
        self.job_title = self._input_to_string(soup, 'VAR_JOBTITLE')
        self.job_code = self._input_to_string(soup, 'VAR_POSITIONTYPE')
        self.date_hired = self._input_to_string(soup, 'DT_DATEHIRED')
        self.date_terminated = self._input_to_string(soup, 'DT_DATETERMINATED')
        self.substitute = self._radio_to_bool(soup, 'BIT_ISSUBSTITUTE')
        self.pending_approval = self._radio_to_bool(soup, 'BIT_EMAILADMINNOTIFICATION')
        self.approval_changes = self._radio_to_bool(soup, 'BIT_EMAILNOTIFICATION')
        self.new_activities = self._radio_to_bool(soup, 'BIT_EMAILNEWACTIVITIES')
        self.upcoming_activities = self._radio_to_bool(soup, 'BIT_EMAILREMINDEVENTS')
        self.teamroom_postings = self._radio_to_bool(soup, 'BIT_EMAILTEAMROOM')
        self.num_of_days = self._input_to_string(soup, 'INT_EMAILREMINDDAYS')
        self.html_format = self._radio_to_bool(soup, 'BIT_EMAILHTMLBODY')
        self.buildings = self._checkboxes_to_list(soup, 'INT_BUILDINGID')
        self.departments = self._checkboxes_to_list(soup, 'INT_DEPARTMENTID')
        self.grades = self._checkboxes_to_list(soup, 'INT_GRADEID')
        self.groups = self._checkboxes_to_list(soup, 'INT_GROUPID')
        self.budget_codes = self._checkboxes_to_list(soup, 'INT_FUNDINGID')

    def __repr__(self):
        return (
            "User "
            "pg_id={} "
            "first_name={} "
            "last_name={} "
            "email={} "
            "active={}"
        ).format(
            self.pg_id,
            self.first_name,
            self.last_name,
            self.email,
            self.active
        )
