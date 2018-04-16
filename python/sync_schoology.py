import logging
import asyncio
import AR.AR as AR
import AR.schoology as schoology
import click
import pprint
import re
from AR.tables import StaffJobRole, DistrictTeacher

pp=pprint.PrettyPrinter()

@click.command()
@click.argument('db_file', type=click.Path(exists=True), metavar='DB_FILE')
@click.option('--debug', is_flag=True, help='Print debugging statements')
def sync(db_file, debug):
    """Syncs up Schoology with a Genesis Database

    DB_FILE - A sqlite3 file of the Genesis database"""

    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    db_session = AR.init(db_file)
    schoology.init()

    # Make sure our buildings are setup correctly
    # NOTE: Genesis uses the term 'schools' to refer to the individual
    # buildings, Schoology uses buildings. In Schoology there is one school,
    # 'Monroe Township Schools' and lots of buildings.
    print('Syncing buildings between Genesis / Schoology...')
    buildings = AR.schools()
    for building in buildings:
        response = schoology.create_update_building(
            title=building.school_name,
            building_code=building.building_code,
            address1=building.school_address1,
            address2=building.school_address2,
            phone=building.school_office_phone,
            website=building.school_url
        )

    # Make queries for teachers, admins, and sysadmins
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
        logging.error("The following IDs show up in multiple user roles: {}",
            ",".join(overlap))
        exit(1)

    print('{} students {} teachers, {} admins, {} sysadmins'.format(
        students.count(), teachers.count(), admins.count(), sysadmins.count()))

    print('Creating Schoology user objects...')
    users = []
    total = students.count() + teachers.count()
    for student in students:
        user = schoology.create_user_object(
            school_uid=student.student_id,
            email=student.email,
            name_first=student.first_name,
            name_last=student.last_name,
            role='Student'
        )
        users.append(user)
        current = len(users)
        if (current % 100) == 0:
            print('{}/{}'.format(current, total))
    for teacher in teachers:
        user = schoology.create_user_object(
            school_uid=teacher.teacher_id,
            email=teacher.email,
            name_first=teacher.first_name,
            name_last=teacher.last_name,
            role='Teacher'
        )
        users.append(user)
        current = len(users)
        if (current % 100) == 0:
            print('{}/{}'.format(current, total))

    #print('Updating / Creating users in Schoology...')
    #complete = 0
    #for user_responses in schoology.bulk_create_update_users(users):
    #    for user_response in user_responses:
    #        if user_response['response_code'] != 200:
    #            pp.pprint(user_response)
    #    complete += len(user_responses)
    #    print('{}/{} users completed'.format(complete, len(users)))

    #print('Creating a set of all users in Schoology...')
    #schoology_ids = { user['school_uid'] for user in schoology.get_users() }
    #deletes = schoology_ids - student_ids - teacher_ids - admin_ids - sysadmin_ids
    #print('Recommend deleting: {}'.format(deletes))

if __name__ == '__main__':
    sync()
