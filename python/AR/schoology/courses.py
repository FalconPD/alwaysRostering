import asyncio
import logging
from AR.schoology import constants

class Courses():
    """Class for dealing with Courses"""

    add_queue = []
    session = None

    async def __aenter__(self):
        self.session = SchoologySession
        return self

    async def __aexit__(self, *exc):
        """Since this has a final flush that may need to occur it's implemented
        as a context manager"""

        await self.flush()

    async def add_update(self, building_code, title, course_code, sections=[]):
        """Takes a list of courses and adds/updates them"""

        building_id = buildings.lookup_id(building_code)
        if building_id == None:
            logging.error('Unable to look up building_code {}'.format(building_code))
            exit(1)

        course = {
            'building_id': building_id,
            'title': title,
            'course_code': course_code,
            'synced': 1,
        }
        if len(sections) > 0:
            course['sections'] = { 'section': [] }
        for section in sections:
            course['sections']['section'].append({
                'title': section['title'],
                'section_school_code': section['section_school_code'],
                'grading_periods': [556703], #TODO: Setup and pull grading periods
                                             #from SchoolAttendanceCycle in Genesis
                'synced': 1
            })

        self.add_queue.append(course)
        if len(self.add_queue) == constants.CHUNK_SIZE:
            await self.flush()

    async def flush(self):
        """Clears out the queues by making bulk requests"""

        if len(self.add_queue) > 0:
            params = { 'update_existing': 1 }
            json_data = { 'courses' : { 'course': self.add_queue }} 
            await utils.post('courses/', json=json_data, params=params)
            self.add_queue = []

#async def list_courses(building_code=None):
#    """Lists all the courses. You can optionally specify a building"""
#
#    logging.debug('Listing courses in Schoology')
#
#    # couldnt' figure out a nice, clean way to do this with the params argument
#    url = baseURL + 'courses' 
#    if building_code:
#        building_id = lookup_building_id(building_code)
#        if building_id == None:
#            logging.error('list_courses: Unable to look up building_code {}'
#                .format(building_code))
#            exit(1)
#        url += '?building_id=' + str(building_id)
#
#    async for response in list_pages(url):
#        yield response['course']
#
#async def bulk_delete_courses(course_ids):
#    """Takes a group of course IDs and deletes them"""
#
#    bulk_length_check(course_ids)
#
#    params = { 'course_ids': ','.join(map(str, course_ids)) }
#    async with session.delete(baseURL + 'courses', params=params,
#        headers=create_header()) as resp: 
#        await handle_status(resp)
