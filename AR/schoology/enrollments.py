from AR.schoology.queue import Queue

class Enrollments():
    """
    Handles our enrollments. NOTE: adds and deletes go in the same queue in
    enrollments and all get processed
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
        Create our queue
        """
        self.enrollments = Queue(self.send)
        return self

    async def __aexit__(self, *exc):
        """
        Flush the queue
        """
        await self.enrollments.flush()

    async def add(self, section_school_code, school_uid, admin=False):
        """
        Adds a user to a section
        """
        await self.enroll(section_school_code, school_uid, admin, delete=False)

    async def delete(self, section_school_code, school_uid, admin=False):
        """
        Deletes a user from a section
        """
        await self.enroll(section_school_code, school_uid, admin, delete=True)

    async def enroll(self, section_school_code, school_uid, admin, delete):
        """
        Create an enrollment and put it in the queue
        """
        enrollment = {
            'section_school_code': section_school_code,
            'school_uid': school_uid
        }
        if admin:
            enrollment['admin'] = '1'
        if delete:
            enrollment['delete'] = '1'
        await self.enrollments.add(enrollment)

    async def send(self, enrollments):
        """
        POSTs a group of enrollments
        """
        json_data = { 'enrollments': { 'enrollment': enrollments } }
        await self.session.post('enrollments/import/course', json=json_data)

    async def list(self, section_id):
        """
        Lists all the course enrollment data for a section from Schoology. Also
        bumps up the page size to perform faster.
        """
        endpoint = 'section/' + str(section_id) + '/enrollments?start=0&limit=200'
        async for response in self.session.list_pages(endpoint):
            yield response['enrollment']
