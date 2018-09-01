class CourseSections():
    """
    Class for dealing with course sections
    """
    @classmethod
    async def create(cls, session):
        """
        Factory function for creating this class
        """
        self = cls()
        self.session = session
        return self

    async def __aenter__(self):
        """
        Does nothing... yet
        """
        return self

    async def __aexit__(self, *exc):
        """
        Does nothing... yet
        """

    async def list(self, course_id):
        """
        Lists all the sections for a given course ID
        """
        endpoint = 'courses/' + str(course_id) + '/sections'
        async for response in self.session.list_pages(endpoint):
            yield response['section']

#    def create_section_object(title, section_school_code):
#        """Creates a Schoology Course Section object"""
#        
#        return {
#            'title': title,
#            'section_school_code': section_school_code,
#            'grading_periods': [1626830909], #TODO: Setup and pull grading periods from SchoolAttendanceCycle in Genesis
#            'synced': 1
#        }
#
#    async def bulk_delete_sections(section_ids):
#        """Takes a group of section IDs and deletes them"""
#
#        bulk_length_check(section_ids)
#
#        params = { 'section_ids': ','.join(map(str, section_ids)) }
#        async with session.delete(baseURL + 'sections', params=params,
#            headers=create_header()) as resp: 
#            await handle_status(resp)
#
