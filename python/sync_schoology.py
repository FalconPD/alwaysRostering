import logging
import asyncio
import aiohttp
import AR.AR as AR
import AR.schoology as schoology
import click
import pprint
import re

pp=pprint.PrettyPrinter()

chunk_size = 50

@click.command()
@click.argument('db_file', type=click.Path(exists=True), metavar='DB_FILE')
@click.option('--debug', is_flag=True, help='Print debugging statements')
def main(db_file, debug):
    """Syncs up Schoology with a Genesis Database

    DB_FILE - A sqlite3 file of the Genesis database"""

    loop = asyncio.get_event_loop()

    if debug:
        logging.basicConfig(level=logging.DEBUG)
#        loop.set_debug(True)
#        http.client.HTTPConnection.debuglevel = 1
#        logging.basicConfig()
#        logging.getLogger().setLevel(logging.DEBUG)
#        requests_log = logging.getLogger("requests.packages.urllib3")
#        requests_log.setLevel(logging.DEBUG)
#        requests_log.propagate = True
    else:
        logging.basicConfig(level=logging.WARNING)

    loop.run_until_complete(sync(loop=loop, db_file=db_file))
    loop.close()

async def create_task(tasks, loop, function):
    """Little wrapper to make and start a task and print status"""

    tasks.append(
        loop.create_task(function)
    )
    await asyncio.sleep(0) # give the task a chance to start
    if len(tasks) % 500 == 0:
        print('{} tasks created'.format(len(tasks)))
    return tasks

async def sync_buildings(loop):
    """Makes sure our buildings are setup correctly"""

    # NOTE: Genesis uses the term 'schools' to refer to the individual
    # buildings, Schoology uses buildings. In Schoology there is one school,
    # 'Monroe Township Schools' and currently 8 buildings (AES, BBS, BES, etc.)
    print('Creating / Updating buildings in Schoology...')
    tasks=[]
    for building in AR.schools():
        await create_task(tasks, loop,
            schoology.buildings.create_update(
                title=building.school_name,
                building_code=building.building_code,
                address1=building.school_address1,
                address2=building.school_address2,
                phone=building.school_office_phone,
                website=building.school_url
            )
        )
    await asyncio.gather(*tasks)
    await schoology.buildings.load()

def create_user_queries():
    """Creates Genesis queries for user group and performs sanity checks"""

    print('Creating Genesis queries for users...')
    students = AR.students()
    teachers = AR.teachers()
    admins = AR.admins()
    sysadmins = AR.sysadmins()

    # Users can only have one role. This keeps users in their highest
    # privelaged role (sysadmin > admin > teacher)
    teachers = teachers.except_(admins)
    teachers = teachers.except_(sysadmins)
    admins = admins.except_(sysadmins)
   
    # Make sure there is no overlap between staff and student IDs
    student_ids = { student.student_id for student in students }
    staff_ids = { staff.teacher_id for staff in
        teachers.union(admins).union(sysadmins) }
    overlap = student_ids & staff_ids
    if  len(overlap) > 0:
        logging.error('The following IDs show up in multiple user roles: {}',
            ','.join(map(str, overlap)))
        exit(1)
    all_ids = student_ids | staff_ids

    print('{} students {} teachers, {} admins, {} sysadmins: {} total IDs'.format(
        students.count(), teachers.count(), admins.count(), sysadmins.count(),
        len(all_ids)))

    return (students, teachers, admins, sysadmins, all_ids)

async def delete_user_accounts(loop, all_ids):
    """Takes a set of all valid genesis IDs and deletes users in Schoology
    that aren't in that set."""

    print('Deleting users with unknown IDs in Schoology')
    checked = 0
    async for page in schoology.users.list():
        for user in page:
            if user['school_uid'] not in all_ids:
                print('Unknown ID {} {} {} (Schoology ID {})'.format(
                    user['id'], user['name_first'], user['name_last'],
                    user['school_uid']))
                await schoology.users.delete(user['id'])
        checked += len(page)
        if checked % 500 == 0:
            print('{} IDs checked'.format(checked))
    await schoology.users.flush()

async def create_user_accounts(loop, students, teachers, admins, sysadmins):
    """Creates / Updates user accounts for students, teachers, admins, and
    sysadmins"""

    tasks=[]
    print('Creating / Updating students in Schoology...')
    for student in students:
        tasks = await create_task(tasks, loop, 
            schoology.users.create_update(
                school_uid=student.student_id,
                name_first=student.first_name,
                name_last=student.last_name,
                email=student.email,
                role='Student'
            )
        )
    print('Creating / Updating teachers in Schoology...')
    for teacher in teachers:
        tasks = await create_task(tasks, loop,
            schoology.users.create_update(
                school_uid=teacher.teacher_id,
                name_first=teacher.first_name,
                name_last=teacher.last_name,
                email=teacher.email,
                role='Teacher'
            )
        )
    print('Creating / Updating admins in Schoology...')
    for admin in admins:
        tasks = await create_task(tasks, loop,
            schoology.users.create_update(
                school_uid=admin.teacher_id,
                email=admin.email,
                name_first=admin.first_name,
                name_last=admin.last_name,
                role='Administrator'
            )
        )
    print('Creating / Updating sysadmins in Schoology...')
    for sysadmin in sysadmins:
        tasks = await create_task(tasks, loop,
            schoology.users.create_update(
                school_uid=sysadmin.teacher_id,
                email=sysadmin.email,
                name_first=sysadmin.first_name,
                name_last=sysadmin.last_name,
                role='Sysadmin'
            )
        )
    await asyncio.gather(*tasks)
    await schoology.users.flush()

def create_courses():
    """Returns Schoology course objects based on the AR.courses() query
    in groups of 50"""

    courses = []    
    for course in AR.courses():
        # Create the course
        schoology_course = schoology.create_course_object(
            building_code = course.school_code,
            title = course.course_description,
            course_code = course.school_code + ' ' + course.course_code
        )

        # Add in the sections
        schoology_course['sections'] = { 'section': [] }
        for section in course.sections:
            schoology_course['sections']['section'].append(
                schoology.create_section_object(
                    title=section.name,
                    section_school_code=section.section_school_code
                )
            )

        # Add it to our list
        courses.append(schoology_course)
        if len(courses) == 50:
            yield courses
            courses = []

    if len(courses) > 0:
        yield courses

async def sync_courses():
    """Creates / updates courses in Schoology. NOTE: This DOES NOT delete
    courses. If someone makes a special courses for whatever reason, it
    remains"""

    total = 0;
    for courses in create_courses():
        response = await schoology.bulk_create_update_courses(courses)
        total += len(courses)
        print('{} courses created / updated'.format(total))

def create_enrollments():
    """Yields student enrollments in blocks of 50"""

    enrollments = []

    for course in AR.courses():
        for section in course.sections:
            for student in section.active_students:
                enrollments.append(
                    schoology.enrollments.create_object(
                        section_school_code=section.section_school_code,
                        school_uid=student.student_id
                    )
                )
                if len(enrollments) == 50:
                    yield enrollments
                    enrollments = []
    if len(enrollments) > 0:
        yield enrollments

async def enroll_students():
    """Enrolls students in Schoology"""

    for enrollments in create_enrollments():
        pp.pprint(enrollments)

async def sync(loop, db_file):
    """Performs all steps to sync Schoology with a Genesis Database"""

    AR.init(db_file)
    await schoology.utils.init(loop)

    #await sync_buildings(loop)
    (students, teachers, admins, sysadmins, all_ids) = create_user_queries()
    #await create_user_accounts(loop, students, teachers, admins, sysadmins)
    await delete_user_accounts(loop, all_ids)
#    await sync_courses()

#    await enroll_students()
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

    await schoology.utils.session.close()

if __name__ == '__main__':
    main()
