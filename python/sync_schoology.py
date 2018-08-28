import logging
import asyncio
import AR.AR as AR
import AR.schoology as schoology
import click
import pprint

pp=pprint.PrettyPrinter()

@click.command()
@click.argument('db_file', type=click.Path(exists=True), metavar='DB_FILE')
@click.option('--debug', is_flag=True, help='Print debugging statements')
def main(db_file, debug):
    """Syncs up Schoology with a Genesis Database

    DB_FILE - A sqlite3 file of the Genesis database"""

    loop = asyncio.get_event_loop()

    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    loop.run_until_complete(sync(loop=loop, db_file=db_file))
    loop.close()

async def create_task(tasks, loop, function):
    """Little wrapper to make a task, start a task, and print status"""

    tasks.append(
        loop.create_task(function)
    )
    await asyncio.sleep(0) # give the task a chance to start
    if len(tasks) % 500 == 0:
        print('{} tasks created'.format(len(tasks)))
    return tasks

async def add_update_buildings(loop, Schoology):
    """Makes sure our buildings are setup correctly"""

    # NOTE: Genesis uses the term 'schools' to refer to the individual
    # buildings, Schoology uses buildings. In Schoology there is one school,
    # 'Monroe Township Schools' and currently 8 buildings (AES, BBS, BES, etc.)
    print('Adding / Updating buildings in Schoology...')
    async with Schoology.Buildings as Buildings:
        tasks=[]
        for building in AR.schools():
            await create_task(tasks, loop,
                Buildings.add_update(
                    title=building.school_name,
                    building_code=building.building_code,
                    address1=building.school_address1,
                    address2=building.school_address2,
                    phone=building.school_office_phone,
                    website=building.school_url
                )
            )
        await asyncio.gather(*tasks)

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

async def delete_users(loop, all_ids, Schoology):
    """
    Takes a set of all valid genesis IDs and deletes users in Schoology
    that aren't in that set.
    """
    print('Deleting users with unknown IDs in Schoology')
    async with Schoology.Users as Users:
        checked = 0
        async for page in Users.list():
            for user in page:
                if user['school_uid'] not in all_ids:
                    print('Unknown ID {} {} {} (Schoology ID {})'.format(
                        user['id'], user['name_first'], user['name_last'],
                        user['school_uid']))
                    await Users.delete(user['id'])
            checked += len(page)
            if checked % 500 == 0:
                print('{} IDs checked'.format(checked))

async def add_update_users(loop, students, teachers, admins, sysadmins,
    Schoology):
    """Adds / Updates user accounts for students, teachers, admins, and
    sysadmins"""

    async with Schoology.Users as Users:
        tasks=[]
        print('Adding / Updating students in Schoology...')
        for student in students:
            tasks = await create_task(tasks, loop, 
                Users.add_update(
                    school_uid=student.student_id,
                    name_first=student.first_name,
                    name_last=student.last_name,
                    email=student.email,
                    role='Student'
                )
            )
        print('Adding / Updating teachers in Schoology...')
        for teacher in teachers:
            tasks = await create_task(tasks, loop,
                Users.add_update(
                    school_uid=teacher.teacher_id,
                    name_first=teacher.first_name,
                    name_last=teacher.last_name,
                    email=teacher.email,
                    role='Teacher'
                )
            )
        print('Adding / Updating admins in Schoology...')
        for admin in admins:
            tasks = await create_task(tasks, loop,
                Users.add_update(
                    school_uid=admin.teacher_id,
                    email=admin.email,
                    name_first=admin.first_name,
                    name_last=admin.last_name,
                    role='Administrator'
                )
            )
        print('Adding / Updating sysadmins in Schoology...')
        for sysadmin in sysadmins:
           tasks = await create_task(tasks, loop,
                Users.add_update(
                    school_uid=sysadmin.teacher_id,
                    email=sysadmin.email,
                    name_first=sysadmin.first_name,
                    name_last=sysadmin.last_name,
                    role='Sysadmin'
                )
            )
        await asyncio.gather(*tasks)

async def add_update_courses(loop, Schoology):
    """
    Adds / Updates courses in Schoology
    """
    print('Adding / Updating {} courses...'.format(AR.courses().count()))

    async with Schoology.Courses as Courses:
        tasks = []
        for course in AR.courses():
            building_code = course.school_code
            title = course.course_description
            course_code = course.school_code + ' ' + course.course_code
            sections = []
            for section in course.sections:
                sections.append({
                    'title': section.name,
                    'section_school_code': section.section_school_code
                })
            tasks = await create_task(tasks, loop,
                Courses.add_update(building_code, title, course_code, sections)
            )
        await asyncio.gather(*tasks)

async def enroll(loop, Schoology):
    """
    Enrolls teachers and students in their courses
    """
    print('Enrolling students and teachers in courses...')

    async with Schoology.Enrollments as Enrollments:
        tasks = []
        for course in AR.courses():
            for section in course.active_sections:
                print('section_school_code={} school_uid={} admin={}'.format(
                    section.section_school_code,
                    section.first_subsection.teacher_id, True)) 
                for student in section.active_students:
                    print('section_school_code={} school_uid={} admin={}'.format(
                        section.section_school_code, student.student_id, False))

async def sync(loop, db_file):
    """
    Performs all steps to sync Schoology with a Genesis Database
    """
    AR.init(db_file)
    async with schoology.Session() as Schoology:
        #await add_update_buildings(loop, Schoology)
        #(students, teachers, admins, sysadmins, all_ids) = create_user_queries()
        #wait add_update_users(loop, students, teachers, admins, sysadmins,
        #    Schoology)
        #await delete_users(loop, all_ids, Schoology)
        #await add_update_courses(loop, Schoology)
        await enroll(loop, Schoology)

if __name__ == '__main__':
    main()
