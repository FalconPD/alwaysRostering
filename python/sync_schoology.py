import logging
import asyncio
from AR.tables import DistrictTeacher, StaffJobRole
import AR.AR as AR
import AR.schoology as schoology
import click
import pprint

pp=pprint.PrettyPrinter()

def print_staff(db_session, staff_id):

    query = (
                db_session.query(DistrictTeacher)
                .filter(DistrictTeacher.teacher_id == staff_id)
                .first()
            )
    print("[{}] {} {}".format(query.teacher_id, query.teacher_first_name, query.teacher_last_name))

def find_deletes(db_session):
    """Get a list of all users from schoology and check to make sure their staff
    or student ID is in Genesis"""

    users = schoology.get_users()
    for user in users:
        print(user.school_uid)

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

    pp.pprint(schoology.get_roles())

    db_session = AR.init(db_file)

    admin_job_codes = ['0102', '0122', '0201', '0202', '0221', '0222', '0231',
        '0232', '0306', '0310', '0312', '0314', '0315', '0319', '0321', '0322',
        '0324', '0399', '0524', '2410', '9000', '9200']
    teacher_job_codes = ['1001', '1003', '1004', '1007', '1015', '1017', '1018',
        '1102', '1103', '1104', '1106', '1150', '1200', '1273', '1283', '1301',
        '1308', '1315', '1317', '1331', '1345', '1401', '1485', '1500', '1510',
        '1530', '1540', '1550', '1607', '1630', '1700', '1706', '1760', '1805',
        '1812', '1821', '1856', '1897', '1901', '1962', '2100', '2110', '2130',
        '2202', '2206', '2231', '2235', '2236', '2302', '2322', '2400', '2401',
        '2405', '2406']
    
    # Load the real, active staff with their job role
    query = (
            db_session.query(DistrictTeacher, StaffJobRole)
            .filter(DistrictTeacher.employment_status == 'A')
            .filter(DistrictTeacher.shared_teacher  == False)
            .filter(DistrictTeacher.state_id_number != '')
            .join(StaffJobRole)
    )

    # Make sets of teacher and admin ids
    admin_ids = {
        staff.teacher_id for staff, job_role in (
            query.filter(StaffJobRole.job_code.in_(admin_job_codes))
        )
    }
    teacher_ids = {
        staff.teacher_id for staff, job_role in (
            query.filter(StaffJobRole.job_code.in_(teacher_job_codes))
        )
    }

    for id in admin_ids:
        print_staff(db_session, id)
    for id in teacher_ids:
        print_staff(db_session, id)

if __name__ == '__main__':
    sync()
