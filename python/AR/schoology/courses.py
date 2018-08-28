from AR.schoology.queue import AddDel

class Courses(AddDel):
    """Class for dealing with Courses"""

    async def add_update(self, building_code, title, course_code, sections=[]):
        """Takes a list of courses and adds/updates them"""

        building_id = self.session.Buildings.lookup_id(building_code)

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
                'grading_periods': [589077], #TODO: Setup and pull grading periods
                                             #from SchoolAttendanceCycle in Genesis
                'synced': 1
            })

        await self.adds.add(course)

    async def send_adds(self, adds):
        """Sends out a request to add courses"""

        params = { 'update_existing': 1 }
        json_data = { 'courses' : { 'course': adds }} 
        await self.session.post('courses/', json=json_data, params=params)

    async def send_dels(self, dels):
        """Sends out a request to delete courses"""

        params = { 'course_ids': ','.join(map(str, dels)) }
        await self.session.delete('courses', params=params)

    async def list(self, building_code=None):
        """Lists all the courses. You can optionally specify a building"""

        # couldnt' figure out a nice, clean way to do this with the params argument
        endpoint = 'courses' 
        if building_code:
            building_id = lookup_building_id(building_code)
            endpoint += '?building_id=' + str(building_id)

        async for response in self.session.list_pages(endpoint):
            yield response['course']

# This snippet deletes all courses (or at least tries to)
#    async for courses in schoology.list_courses():
#        await asyncio.sleep(0.25)
#        course_ids=[]
#        for course in courses:
#            print('{}'.format(course['title']))
#            course_ids.append(course['id'])
#            async for sections in schoology.list_sections(course_id=course['id']):
#                await asyncio.sleep(0.25)
#                section_ids=[]
#                for section in sections:
#                    print('[{}]  {}'.format(section['id'], section['section_title']))
#                    section_ids.append(section['id'])
#                if len(section_ids) > 0:
#                    await schoology.bulk_delete_sections(section_ids)
#        if len(course_ids) > 0:
#            await schoology.bulk_delete_courses(course_ids)
