import datetime
"""
Constants used by the Professional Growth module
"""
CREDENTIALS_PATH = '../../include/credentials.json'
SELENIUM_TIMEOUT = 10
MAX_RETRIES = 10
MAX_TOKENS = 10
TOKEN_RATE = 10
SUBMITTER_PG_ID = 867245
DATE_FORMAT = '%m/%d/%Y'
DATE_ATTRIBUTES = ['dob', 'date_hired', 'date_terminated']

# Parameters for downloading LearningPlan and Activites tables
START_DATE = datetime.date(2009, 9, 1)
END_DATE = datetime.date.today() + datetime.timedelta(days=365)
TIMEDELTA = datetime.timedelta(days=1500)
