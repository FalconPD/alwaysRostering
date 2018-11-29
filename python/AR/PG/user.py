from bs4 import BeautifulSoup
from multidict import MultiDict
import logging
import datetime

from AR.PG import constants

class User():
    """
    A representation of a Professional Growth user
    """
    def _input_to_string(self, soup, id):
        """
        Returns the value of an input as a string
        """
        return soup.find('input', id=id)['value']

    def _string_to_date(self, string):
        """
        Returns a string from a date
        """
        if string == '':
            return None
        return datetime.datetime.strptime(string, constants.DATE_FORMAT)

    def _input_to_date(self, soup, id):
        """
        Returns the value of an input as a date
        """
        string = self._input_to_string(soup, id)
        if string == '':
            return None
        return self._string_to_date(string)

    def _checkboxes_to_dict(self, soup, for_attr):
        """
        Creates a dict from a checkbox group
        """
        our_dict = {}
        for label in soup('label', attrs={'for': for_attr,
            'class': 'iform-label_checkbox'}):
            our_input = label.find('input')
            if our_input.has_attr('checked'):
                name = list(label.strings)[0]
                our_dict[our_input['value']] = name
        return our_dict

    def _radio_to_bool(self, soup, base_id):
        """
        Returns a boolean value from a radio button. Checks the "Yes" button
        """
        return soup.find('input', id=base_id+'_Yes').has_attr('checked')

    def _from_html(self, html):
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
        self.catalogs = self._checkboxes_to_dict(soup, 'INT_PROGRAMADMINID')
        self.certificate_holder = self._radio_to_bool(soup, 'BIT_ISINSTRUCTIONAL')
        self.ssn = self._input_to_string(soup, 'ENC_SID')
        self.certificate_id = self._input_to_string(soup, 'VAR_CERTIFICATEID')
        self.certificate_expiration = self._input_to_string(soup, 'DT_CERTIFICATEEXPIRATIONDATE')
        self.dob = self._input_to_date(soup, 'DT_DATEOFBIRTH')
        self.job_title = self._input_to_string(soup, 'VAR_JOBTITLE')
        self.job_code = self._input_to_string(soup, 'VAR_POSITIONTYPE')
        self.payroll_id = self._input_to_string(soup, 'VAR_EMPLOYEEID')
        self.date_hired = self._input_to_date(soup, 'DT_DATEHIRED')
        self.date_terminated = self._input_to_date(soup, 'DT_DATETERMINATED')
        self.substitute = self._radio_to_bool(soup, 'BIT_ISSUBSTITUTE')
        self.pending_approval = self._radio_to_bool(soup, 'BIT_EMAILADMINNOTIFICATION')
        self.approval_changes = self._radio_to_bool(soup, 'BIT_EMAILNOTIFICATION')
        self.new_activities = self._radio_to_bool(soup, 'BIT_EMAILNEWACTIVITIES')
        self.upcoming_activities = self._radio_to_bool(soup, 'BIT_EMAILREMINDEVENTS')
        self.teamroom_postings = self._radio_to_bool(soup, 'BIT_EMAILTEAMROOM')
        self.num_of_days = self._input_to_string(soup, 'INT_EMAILREMINDDAYS')
        self.html_format = self._radio_to_bool(soup, 'BIT_EMAILHTMLBODY')
        self.buildings = self._checkboxes_to_dict(soup, 'INT_BUILDINGID')
        self.departments = self._checkboxes_to_dict(soup, 'INT_DEPARTMENTID')
        self.grades = self._checkboxes_to_dict(soup, 'INT_GRADEID')
        self.groups = self._checkboxes_to_dict(soup, 'INT_GROUPID')
        self.budget_codes = self._checkboxes_to_dict(soup, 'INT_FUNDINGID')

    def _from_dict(self, dict_):
        """
        Sets up a user instance from a dict
        """
        for key, value in dict_.items():
            if key in constants.DATE_ATTRIBUTES:
                value = self._string_to_date(value)
            setattr(self, key, value)

    def to_dict(self):
        """
        Returns a JSON serializable dict of this class
        """
        dict_ = {}
        for key, value in self.__dict__.items():
            if key in constants.DATE_ATTRIBUTES: 
                value = self._date_to_string(value)
            dict_[key] = value
        return dict_
        

    def _from_teacher(self, teacher):
        """
        Constructs a NEW user object from an AR teacher object with
        reasonable default values
        """
        self.pg_id = None
        self.first_name = teacher.teacher_first_name
        self.last_name = teacher.teacher_last_name
        self.email = teacher.email
        self.instructor = False
        self.admin = False
        self.active = True
        self.catalogs = {}
        self.certificate_holder = teacher.certification_status
        self.ssn = ""
        self.certificate_id = teacher.state_id_number
        self.certificate_expiration = ""
        self.dob = teacher.date_of_birth
        self.job_title = ""
        self.job_code = ", ".join([job_role.job_code for job_role in teacher.job_roles])
        self.payroll_id = teacher.other_id_number
        self.date_hired = teacher.employment_records[0].start_date
        self.date_terminated = teacher.employment_records[-1].end_date
        self.substitute = False
        self.pending_approval = True
        self.approval_changes = True
        self.new_activities = True
        self.upcoming_activities = True
        self.teamroom_postings = True
        self.num_of_days = 5
        self.html_format = True
        self.buildings = {}
        self.departments = {}
        self.grades = {}
        self.groups = {}
        self.budget_codes = {}

    def __init__(self, html=None, dict_=None, teacher=None):
        """
        Lets you create a user object from either HTML, a dictionary, or
        nothing
        """
        if html != None:
            self._from_html(html)
        elif dict_ != None:
            self._from_dict(dict_)
        elif teacher != None:
            self._from_teacher(teacher)

    def _yes_no(self, flag):
        """
        Returns a 'Yes' or 'No' string for a boolean
        """
        if flag:
            return 'Yes'
        return 'No'
   
    def _date_to_string(self, date):
        """
        Converts from a python datetime to a string format that PG likes
        """
        if date != None:
            return date.strftime(constants.DATE_FORMAT)
        return ''
 
    def data(self):
        """
        Returns a MultiDict (needed for lists) used by the save operation
        """
        dict_ = MultiDict()
        dict_.add('RURL', '')    
        dict_.add('M', 'E')
        dict_.add('AID', 0)
        dict_.add('O', constants.SUBMITTER_PG_ID)
        dict_.add('F', 10045) # the ID of the form we are submitting
        dict_.add('I', self.pg_id if self.pg_id != None else 0)
        dict_.add('VAR_FIRSTNAME', self.first_name)
        dict_.add('VAR_LASTNAME', self.last_name)
        dict_.add('VAR_EMAIL', self.email)
        dict_.add('BIT_ISINSTRUCTOR', self._yes_no(self.instructor))
        dict_.add('BIT_ISDISTRICTADMIN', self._yes_no(self.admin))
        dict_.add('BIT_ACTIVE', self._yes_no(self.active))
        for key in self.catalogs.keys():
            dict_.add('INT_PROGRAMADMINID', key)
        dict_.add('BIT_ISINSTRUCTIONAL', self._yes_no(self.certificate_holder))
        dict_.add('ENC_SID', self.ssn)
        dict_.add('VAR_CERTIFICATEID', self.certificate_id)
        dict_.add('DT_CERTIFICATEEXPIRATIONDATE', self.certificate_expiration)
        dict_.add('DT_DATEOFBIRTH', self._date_to_string(self.dob))
        dict_.add('VAR_JOBTITLE', self.job_title)
        dict_.add('VAR_POSITIONTYPE', self.job_code)
        dict_.add('VAR_EMPLOYEEID', self.payroll_id)
        dict_.add('DT_DATEHIRED', self._date_to_string(self.date_hired))
        dict_.add('DT_DATETERMINATED', self._date_to_string(self.date_terminated))
        dict_.add('BIT_ISSUBSTITUTE', self._yes_no(self.substitute))
        dict_.add('BIT_EMAILADMINNOTIFICATION',
            self._yes_no(self.pending_approval))
        dict_.add('BIT_EMAILNOTIFICATION', self._yes_no(self.approval_changes))
        dict_.add('BIT_EMAILNEWACTIVITIES', self._yes_no(self.new_activities))
        dict_.add('BIT_EMAILREMINDEVENTS',
            self._yes_no(self.upcoming_activities))
        dict_.add('BIT_EMAILTEAMROOM', self._yes_no(self.teamroom_postings))
        dict_.add('INT_EMAILREMINDDAYS', self.num_of_days)
        dict_.add('BIT_EMAILHTMLBODY', self._yes_no(self.html_format))
        for key in self.buildings.keys():
            dict_.add('INT_BUILDINGID', key)
        for key in self.departments.keys():
            dict_.add('INT_DEPARTMENTID', key)
        for key in self.grades.keys():
            dict_.add('INT_GRADEID', key)
        for key in self.groups.keys():
            dict_.add('INT_GROUPID', key)
        for key in self.budget_codes.keys():
            dict_.add('INT_FUNDINGID', key)
        dict_.add('btn_Submit.x', 100)
        return dict_
    
    def __eq__(self, other):
        """
        Checks to see if two users are the same.
        """
        if other == None:
            return False
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Comparing:")
            logging.debug(self)
            logging.debug(other)
            self_dict = self.__dict__
            other_dict = other.__dict__
            for key in self_dict.keys():
                if self_dict[key] != other_dict[key]:
                    print("{}: {}->{}".format(key, self_dict[key], other_dict[key]))
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return (
            "PG User "
            "pg_id={} "
            "payroll_id={} "
            "first_name={} "
            "last_name={} "
            "email={} "
            "active={}"
        ).format(
            self.pg_id,
            self.payroll_id,
            self.first_name,
            self.last_name,
            self.email,
            self.active
        )
