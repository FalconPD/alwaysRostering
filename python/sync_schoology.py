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

def create_sysadmin(sysadmin):
    """Takes a DistrictTeacher and returns a Schoology user object"""

    return schoology.create_user_object(
        school_uid=sysadmin.teacher_id,
        email=sysadmin.email,
        name_first=sysadmin.first_name,
        name_last=sysadmin.last_name,
        role='Sysadmin'
    )

def create_admin(admin):
    """Takes a DistrictTeacher and returns a Schoology user object"""

    return schoology.create_user_object(
        school_uid=admin.teacher_id,
        email=admin.email,
        name_first=admin.first_name,
        name_last=admin.last_name,
        role='Administrator'
    )

def create_teacher(teacher):
    """Takes a DistrictTeacher and returns a Schoology user object"""

    return schoology.create_user_object(
        school_uid=teacher.teacher_id,
        email=teacher.email,
        name_first=teacher.first_name,
        name_last=teacher.last_name,
        role='Teacher'
    )

def create_student(student):
    """Takes a Student and returns a schoology user object"""

    return schoology.create_user_object(
        school_uid=student.student_id,
        email=student.email,
        name_first=student.first_name,
        name_last=student.last_name,
        role='Student'
    )

def create_users(query, create_function):
    """Takes a query and create function and creates an array of schoology
    users in chunks"""

    users = []
    completed = 0
    for person in query:
        users.append(create_function(person))
        completed += 1
        if completed == chunk_size:
            yield users
            completed = 0
            users = []
    if completed != 0:
        yield users

async def create_update_users(loop, query, create_function):
    """Goes through the results of a query, creating Schoology user objects and
    making tasks to create / update those users in bulk. Also prints a status
    """

    tasks = []
    completed_users = 0
    total_users = query.count()
    for users in create_users(query, create_function):
        tasks.append(
            loop.create_task(schoology.bulk_create_update_users(users))
        )
        await asyncio.sleep(0) # Give the task a chance to run
        completed_users += len(users)
        print('{}/{}'.format(completed_users, total_users))
    responses = await asyncio.gather(*tasks)

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

async def sync_buildings(db_session):
    """Makes sure our buildings are setup correctly"""

    # NOTE: Genesis uses the term 'schools' to refer to the individual
    # buildings, Schoology uses buildings. In Schoology there is one school,
    # 'Monroe Township Schools' and currently 8 buildings (AES, BBS, BES, etc.)
    print('Creating / Updating buildings in Schoology...')
    tasks=[]
    for building in AR.schools():
        tasks.append(
            schoology.create_update_building(
                title=building.school_name,
                building_code=building.building_code,
                address1=building.school_address1,
                address2=building.school_address2,
                phone=building.school_office_phone,
                website=building.school_url
            )
        )
    await asyncio.gather(*tasks)
    await schoology.load_buildings()

def create_user_queries(db_session):
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

async def delete_users(all_ids):
    """Takes a set of all valid genesis IDs and deletes users in Schoology
    that aren't in that set. It goes page by page through the responses
    of the Schoology user list. It deletes in chunks of 50, awaiting the delete
    coroutine to try to avoid a 429 (too many requests) error."""

    print('Deleting users with unknown IDs in Schoology')
    retrieved = 0
    deletes = []
    async for page in schoology.get_users():
        for user in page:
            if user['school_uid'] not in all_ids:
                print('Unknown ID {} {} {} (Schoology ID {})'.format(
                    user['id'], user['name_first'], user['name_last'],
                    user['school_uid']))
                deletes.append(user['id'])
                if len(deletes) > chunk_size:
                    await schoology.bulk_delete_users(deletes[:chunk_size])
                    deletes = deletes[chunk_size:]
        retrieved += len(page)
        print('{} IDs checked'.format(retrieved))
    await schoology.bulk_delete_users(deletes)

async def sync(loop, db_file):
    """Syncs up Schoology with a Genesis Database"""

    db_session = AR.init(db_file)
    await schoology.init(loop)

    # We can sync buildings and create queries at the same time
    task = loop.create_task(sync_buildings(db_session))
    await asyncio.sleep(1) # give the task a chance to start
    (students, teachers, admins, sysadmins, all_ids) = create_user_queries(db_session)
    await task

    # Create user accounts
    responses = []
    print('Creating / Updating students in Schoology...')
    responses.append(await create_update_users(loop, students, create_student))
    print('Creating / Updating teachers in Schoology...')
    responses.append(await create_update_users(loop, teachers, create_teacher))
    print('Creating / Updating admins in Schoology...')
    responses.append(await create_update_users(loop, admins, create_admin))
    print('Creating / Updating sysadmins in Schoology...')
    responses.append(await create_update_users(loop, sysadmins, create_sysadmin))

    # Delete users
    await delete_users(all_ids)

if __name__ == '__main__':
    main()
