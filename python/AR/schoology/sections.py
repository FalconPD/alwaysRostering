"""Functions relating to sections"""

def create_section_object(title, section_school_code):
    """Creates a Schoology Course Section object"""
    
    return {
        'title': title,
        'section_school_code': section_school_code,
        'grading_periods': [1492074755], #TODO: Setup and pull grading periods from SchoolAttendanceCycle in Genesis
        'synced': 1
    }

async def list_sections(course_id):
    """Lists all the sections for a given course ID."""

    logging.debug('Listing sections in {}'.format(course_id))

    url = baseURL + 'courses/' + str(course_id) + '/sections'

    async for response in list_pages(url):
        yield response['section']

async def bulk_delete_sections(section_ids):
    """Takes a group of section IDs and deletes them"""

    bulk_length_check(section_ids)

    params = { 'section_ids': ','.join(map(str, section_ids)) }
    async with session.delete(baseURL + 'sections', params=params,
        headers=create_header()) as resp: 
        await handle_status(resp)

