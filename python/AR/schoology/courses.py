"""Functions relating to courses"""

def create_course_object(building_code, title, course_code, department=None,
    description=None, credits=None, grades=None, subject=None):

    building_id = lookup_building_id(building_code)
    if building_id == None:
        logging.error('Unable to look up building_code {}'.format(building_code))
        exit(1)
    course = {
        'building_id': building_id,
        'title': title,
        'course_code': course_code,
        'synced': 1,
    }
    if department != None:
        course['department'] = department
    if description != None:
        course['description'] = description
    if credits != None:
        course['credits'] = credits
    if grades != None:
        course['credits'] = grades
    if subject != None:
        course['subject'] = subject
    return course

async def bulk_create_update_courses(courses):
    """Takes a list of courses and create/updates them"""

    logging.debug('Bulk creating /updating courses')

    bulk_length_check(courses)

    params = { 'update_existing': 1 }
    json_data = { 'courses': { 'course': courses } }
    async with session.post(baseURL + 'courses/', json=json_data, params=params,
        headers=create_header()) as resp:
        await handle_status(resp)
        return await resp.json()

async def list_courses(building_code=None):
    """Lists all the courses. You can optionally specify a building"""

    logging.debug('Listing courses in Schoology')

    # couldnt' figure out a nice, clean way to do this with the params argument
    url = baseURL + 'courses' 
    if building_code:
        building_id = lookup_building_id(building_code)
        if building_id == None:
            logging.error('list_courses: Unable to look up building_code {}'
                .format(building_code))
            exit(1)
        url += '?building_id=' + str(building_id)

    async for response in list_pages(url):
        yield response['course']

async def bulk_delete_courses(course_ids):
    """Takes a group of course IDs and deletes them"""

    bulk_length_check(course_ids)

    params = { 'course_ids': ','.join(map(str, course_ids)) }
    async with session.delete(baseURL + 'courses', params=params,
        headers=create_header()) as resp: 
        await handle_status(resp)
