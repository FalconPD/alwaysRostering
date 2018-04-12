import logging
import asyncio
from AR.tables import DistrictTeacher, StaffJobRole, Student
import AR.AR as AR
import AR.schoology as schoology
import click
import pprint
import re

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

    print('Creating user sets...')

    # Load all K-12, in-district, active students 
    grade_levels = ['KH', 'KF', '01', '02', '03', '04', '05', '06', '07', '08',
        '09', '10', '11', '12']
    schools = ['AES', 'AMS', 'BBS', 'BES', 'MLS', 'MTHS', 'OTS', 'WLS'] 
    query = (
        db_session.query(Student)
        .filter(Student.enrollment_status == 'ACTIVE')
        .filter(Student.homebound_status == 'NO')
        .filter(Student.grade_level.in_(grade_levels))
        .filter(Student.current_school.in_(schools))
    )
    student_ids = {student.student_id for student in query}

    # Load the real, active, confiured staff with their job role
    # NOTE: Staff will have to have their state_id_number and data_1
    # (network id) set
    query = (
            db_session.query(DistrictTeacher, StaffJobRole)
            .filter(DistrictTeacher.employment_status == 'A')
            .filter(DistrictTeacher.shared_teacher  == False)
            .filter(DistrictTeacher.state_id_number != '')
            .filter(DistrictTeacher.data_1 != '')
            .join(StaffJobRole)
    )

    # Make sets of teacher, admin, and sysadmin ids
    teacher_job_codes = ['1001', '1003', '1004', '1007', '1015', '1017', '1018',
        '1102', '1103', '1104', '1106', '1150', '1200', '1273', '1283', '1301',
        '1308', '1315', '1317', '1331', '1345', '1401', '1485', '1500', '1510',
        '1530', '1540', '1550', '1607', '1630', '1700', '1706', '1760', '1805',
        '1812', '1821', '1856', '1897', '1901', '1962', '2100', '2110', '2130',
        '2202', '2206', '2231', '2235', '2236', '2302', '2322', '2400', '2401',
        '2405', '2406']
    teacher_ids = {
        staff.teacher_id for staff, job_role in (
            query.filter(StaffJobRole.job_code.in_(teacher_job_codes))
        )
    }

    admin_job_codes = ['0102', '0122', '0201', '0202', '0221', '0222', '0231',
        '0232', '0306', '0310', '0312', '0314', '0315', '0319', '0321', '0322',
        '0324', '0399', '0524', '2410']
    admin_ids = {
        staff.teacher_id for staff, job_role in (
            query.filter(StaffJobRole.job_code.in_(admin_job_codes))
        )
    }

    sysadmin_job_codes = ['9200']
    sysadmin_ids = {
        staff.teacher_id for staff, job_role in (
            query.filter(StaffJobRole.job_code.in_(sysadmin_job_codes))
        )
    }
    sysadmin_ids.add('9999') # Director of IT
    sysadmin_ids.add('099') # Ed Tech Facilitator

    # Users can only be in one group. This keeps users in their highest
    # privelaged group (sysadmin > admin > teacher)
    teacher_ids -= (teacher_ids & admin_ids)
    teacher_ids -= (teacher_ids & sysadmin_ids)
    admin_ids -= (admin_ids & sysadmin_ids)

    # Make sure there is no overlap between staff and student IDs
    intersection = student_ids & teacher_ids & admin_ids & sysadmin_ids
    if len(intersection) > 0:
        logging.error("The following IDs show up in multiple sets: {}", ",".join(intersection))

    print('{} students {} teachers, {} admins, {} sysadmins'.format(
        len(student_ids), len(teacher_ids), len(admin_ids), 
        len(sysadmin_ids)))

    # Create a list of Schoology user objects from each set
    users = []
    for teacher_id in teacher_ids:
        teacher = (
            db_session.query(DistrictTeacher)
            .filter(DistrictTeacher.teacher_id == teacher_id)
            .first()
        )

        # Clean the Genesis data if needed

        # Teacher names may be improperly capitalized and kindergarten teachers
        # may have AM/PM after their name
        name_first = teacher.teacher_first_name
        name_last = re.sub(r' (AM|PM)$', '', teacher.teacher_last_name, count=1)
        if name_first.isupper():
            name_first = name_first.title()
        if name_last.isupper():
            name_last = name_last.title()
        if (name_first != teacher.teacher_first_name) or (name_last != teacher.teacher_last_name):
            logging.warning('[{}] Correcting name: {} {} -> {} {}'
                .format(teacher_id, teacher.teacher_first_name,
                teacher.teacher_last_name, name_first, name_last))

        # Teacher emails may be the long form
        # FirstName.LastName@monroe.k12.nj.us instead of
        # network_id@monroe.k12.nj.us. We want the short one as it is
        # guaranteed to be unique.  Also, it should be lowercase.
        email = teacher.data_1.lower() + '@monroe.k12.nj.us'
        if email != teacher.teacher_email:
            logging.warning('[{}] Correcting email: {} -> {}'.format(teacher_id,
                teacher.teacher_email, email))

        user = schoology.create_user_object(
            school_uid=teacher_id,
            email=email,
            name_first=name_first,
            name_last=name_last,
            role='Teacher'
        )
        users.append(user)

    user_responses = schoology.bulk_create_update(users)
    for user_response in user_responses:
        if user_response['response_code'] != 200:
            if 'school_uid' in user_response:
                teacher = (
                    db_session.query(DistrictTeacher)
                    .filter(DistrictTeacher.teacher_id == user_response['school_uid'])
                    .first()
                )
                print('[{}] {} {} {}'.format(teacher.teacher_id,
                    teacher.teacher_first_name, teacher.teacher_last_name,
                    user_response['message']))
            else:
                pp.pprint(user_response)

if __name__ == '__main__':
    sync()
