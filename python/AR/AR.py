import logging
from AR.tables import Base, Student, DistrictTeacher, StaffJobRole, School, CurriculumCourse, CourseSection
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
import re

grade_levels = ['KH', 'KF', '01', '02', '03', '04', '05', '06', '07', '08', '09',
    '10', '11', '12']
school_codes = ['AES', 'AMS', 'BBS', 'BES', 'MLS', 'MTHS', 'OTS', 'WES']
teacher_job_codes = ['1001', '1003', '1004', '1007', '1015', '1017', '1018',
    '1102', '1103', '1104', '1106', '1150', '1200', '1273', '1283', '1301',
    '1308', '1315', '1317', '1331', '1345', '1401', '1485', '1500', '1510',
    '1530', '1540', '1550', '1607', '1630', '1700', '1706', '1760', '1805',
    '1812', '1821', '1856', '1897', '1901', '1962', '2100', '2110', '2130',
    '2202', '2206', '2231', '2235', '2236', '2302', '2322', '2400', '2401',
    '2405', '2406']
admin_job_codes = ['0102', '0122', '0201', '0202', '0221', '0222', '0231',
    '0232', '0306', '0310', '0312', '0314', '0315', '0319', '0321', '0322',
    '0324', '0399', '0524', '2410']
sysadmin_job_codes = ['9200']

db_session = None

def init(db_file):
    global db_session

    logging.debug('Loading database file {}'.format(db_file))
    engine = create_engine('sqlite:///{}'.format(db_file), echo=False)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    db_session = DBSession()
    return db_session

def students():
    """Returns a query of active, in-district students. Defaults to all
    students, but you can specify grade levels and schools"""

    return (
        db_session.query(Student)
        .filter(Student.enrollment_status == 'ACTIVE')
        .filter(Student.homebound_status == 'NO')
        .filter(Student.grade_level.in_(grade_levels))
        .filter(Student.current_school.in_(school_codes))
    )

def staff():
    """Returns a query of real, active staff
    NOTE: state_id_number, data_1 (user_id) have to be set for staff to be
    considered real and active"""

    return (
        db_session.query(DistrictTeacher)
        .filter(DistrictTeacher.employment_status == 'A')
        .filter(DistrictTeacher.shared_teacher  == False)
        .filter(DistrictTeacher.state_id_number != '')
    )

def staff_by_job_codes(job_codes):
    """Returns a query for staff with particular job codes"""

    return (
        staff().filter(DistrictTeacher.job_roles.any(
            StaffJobRole.job_code.in_(job_codes)
        ))
    )

def teachers():
    """Returns a query of teachers"""

    return staff_by_job_codes(teacher_job_codes)

def admins():
    """Returns a query of administrators"""

    return staff_by_job_codes(admin_job_codes)

def sysadmins():
    """Returns a query of sysadmins.
    Manually adds Ed Tech Facilitator and Director of IT by ID"""

    extra_ids = ['099', '9999']
    extra_query = (
        db_session.query(DistrictTeacher)
        .filter(DistrictTeacher.teacher_id.in_(extra_ids))
    )

    return (
        staff_by_job_codes(sysadmin_job_codes).union(extra_query)
    )

def schools():
    """Returns a query of in-district schools"""

    return (
        db_session.query(School)
        .filter(School.building_code.in_(school_codes))
    )

def courses():
    """Returns a query of active courses with sections that have at least one
    student in them. DOES NOT include Homeroom courses"""

    return (
        db_session.query(CurriculumCourse)
        .filter(CurriculumCourse.course_code != '000')
        .filter(CurriculumCourse.course_active == True)
        .filter(CurriculumCourse.school_code.in_(school_codes))
        .filter(CurriculumCourse.sections.any(CourseSection.assigned_seats > 0))
    )
