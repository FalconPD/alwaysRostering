class User():
    """
    A representation of a PG user
    """
    # User info
    first_name = None
    last_name = None
    email = None
    # User configuration
    intructor = False
    admin = False
    active = False
    # Admin rights
    admin_catalogs = []
    # Certificate / Licensure information
    certificate_holder = False
    ssn = None
    certificate_id = None
    certificate_expiration = None
    dob = None
    # Personnel information
    job_title = None
    job_code = None
    employee_number = None
    date_hired = None
    date_terminated = None
    substitute = False
    # PLM Email Notifications Preferences
    pending_approval = False
    approval_status_changes = False
    new_catalog_activities = False
    upcoming_activity_reminders = False
    teamroom_postings = False
    num_of_days = None
    html_format = False
    # Buildings
    buildings = []
    # Departments
    departments = []
