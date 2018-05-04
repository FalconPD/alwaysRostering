from AR.schoology.lookup import Lookup

class GradingPeriods(Lookup):
    """A class for dealing with Grading Periods"""

    endpoint = 'gradingperiods'
    heading = 'gradingperiods'
    lookup_by = 'title'
