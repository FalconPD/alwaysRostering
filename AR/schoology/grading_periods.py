from AR.schoology.lookup import Lookup

class GradingPeriods(Lookup):
    """
    A class for dealing with Grading Periods
    """

    endpoint = 'gradingperiods'
    heading = 'gradingperiods'
    lookup_by = 'title'

    async def create_gp(self, title, start, end):
        """
        Creates a new grading period
        """
        json = {
            'title'        : title,
            'start'        : start.isoformat(),
            'end'          : end.isoformat(),
        }
        await self.session.post('/gradingperiods', json=json)

    async def update(self, id, title, start, end):
        """
        Updates a grading period
        """
        json = {
            'title'        : title,
            'start'        : start.isoformat(),
            'end'          : end.isoformat(),
        }
        await self.session.put(f"/gradingperiods/{id}", json=json) 
