"""
Base module for the alwaysRostering system
"""

# System
import logging
import json
import re
from datetime import date

# Sqlalchemy
from sqlalchemy.sql.expression import func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# alwaysRostering
from AR.tables import Base, Student, DistrictTeacher, StaffJobRole, School
from AR.tables import CurriculumCourse, CourseSection, StaffEmploymentRecord

grade_levels       = ['KH', 'KF', '01', '02', '03', '04', '05', '06', '07',
                      '08', '09', '10', '11', '12']
school_codes       = ['AES', 'BBS', 'BES', 'MLS', 'MTHS', 'MTMS', 'OTS', 'WES']
teacher_job_codes = [
    '1000', # Preschool
    '1001', # Elementary - 8th Grade
    '1003', # Kindergarten
    '1004', # Elementary School Teacher K-5
    '1007', # Elementary Teacher in Secondary Setting
    '1015', # English/Elementary
    '1017', # Science/Elementary
    '1018', # Social Studies/Elementary
    '1102', # Mathematics Grades 5-8
    '1103', # Science Grades 5-8
    '1104', # Social Studies Grades 5-8
    '1106', # Language Arts / Literacy Grades 5-8
    '1150',
    '1200',
    '1273',
    '1283',
    '1301',
    '1308',
    '1315',
    '1317',
    '1331',
    '1345',
    '1401',
    '1485',
    '1500',
    '1510',
    '1530',
    '1540',
    '1550',
    '1607',
    '1630',
    '1700',
    '1706',
    '1760',
    '1805',
    '1812',
    '1821',
    '1856',
    '1897',
    '1901',
    '1962',
    '2100',
    '2110',
    '2130',
    '2202',
    '2206',
    '2231',
    '2235',
    '2236',
    '2302',
    '2305', # Social Studies Humanities
    '2322',
    '2400',
    '2401',
    '2405', # Resource Program In-Class
    '2406',
    '2645', # Television Production
    '3135', # Structured Learning Experience Coordinator
]
principal_job_codes = [
    '0201', # HS Principal
    '0202', # Assistant HS Principal
    '0221', # MS Principal
    '0222', # Assistant MS Principal
    '0231', # Elementary Principal
    '0232', # Assistant Elementary Principal
]
supervisor_job_codes = [
    '0306', # Supervisor PPS
    '0310', # Supervisor Athletics
    '0312', # Supervisor Art
    '0314', # Supervisor English
    '0315', # Supervisor Foreign Languages
    '0319', # Supervisor Mathematics
    '0321', # Supervisor Music
    '0322', # Supervisor Science
    '0324', # Supervisor Special Education
    '0399', # Supervisor Special Project
]
other_admin_job_codes = [
    '0102', # Superintendent
    '0122', # Assistant Superintendent
    '0524', # Director Special Education
    '2410', # Teacher Coach
]
sysadmin_job_codes = [
    '9200' # Technicians
]
edservices_job_codes = [
    '0002', # Counselor (Purchased)
    '0004', # OT (Purchased)
    '3101', # Counselor
    '3105', # Media Specialist
    '3111', # OT
    '3112', # PT
    '3113', # Athletic Trainer
    '3116', # Psychologist
    '3117', # Social Worker
    '3118', # LDTC
    '3119', # Reading Specialist
    '3120', # Speech
    '3121', # Coordinator Substance Abuse
    '3125', # Teacher / Behavior Specialist (SE only)
]
nurse_job_codes = [
    '3114' # School Nurse
]
noncert_job_codes = [
    '0029', # Non-instructional Paraprofessionals (Serving Ages 3-5)
    '0030', # Non-instructional Paraprofessionals (Serving Ages 6-21)
    '0032', # Clerical/Secretarial
    '0033', # Service Workers
    '0035', # Laborers Unskilled
    '0034', # Skilled Craftperson's
    '9000', # Professional Staff
    '9025', # BCBA Behavior Specialist
    '9030', # Data Coordinator
    '9100', # Instructional Paraprofessionals (Serving Ages 3-5)
    '9101', # Instructional Paraprofessionals (Serving Ages 6-21)
    '9150', # Non-instruction Paraprofessionals (Serving Ages 3-5)
    '9151', # Non-instructional Paraprofessionals (Serving Ages 6-21)
    '9200', # Technicians
    '9300', # Clerical/Secretarial
    '9400', # Service Workers
    '9500', # Skilled Craftperson's
    '9600', # Laborers Unskilled
]

db_session = None

def init(db_file):
    global db_session

    logging.debug('Loading database file {}'.format(db_file))
    engine = create_engine('sqlite:///{}'.format(db_file), echo=False)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    db_session = DBSession()

    # HACK: This goes through the database and sets employment_status to L for
    # anyone who has been determined to be on leave
    for teacher in db_session.query(DistrictTeacher):
        # get the latest employment record
        last_record = (
            db_session.query(StaffEmploymentRecord)
            .filter(StaffEmploymentRecord.teacher_id==teacher.teacher_id)
            .group_by(StaffEmploymentRecord.teacher_id)
            .having(func.max(StaffEmploymentRecord.end_date))
            .one_or_none()
        )
        if last_record != None:
            # if they are inactive AND 30 - maternity, 31 - sabbatical, or 32 - other
            if (last_record.exit_code in ['30', '31', '32']) and teacher.employment_status != 'A':
                teacher.employment_status = 'L'

    return db_session

def students():
    """
    Returns a query of active, in-district students.
    """
    return (
        db_session.query(Student)
        .filter(Student.enrollment_status == 'ACTIVE')
        .filter(Student.grade_level.in_(grade_levels))
        .filter(Student.current_school.in_(school_codes))
    )

def staff():
    """
    Returns a query of real staff either (A)CTIVE or on (L)EAVE
    NOTE: state_id_number has to be set for staff to be considered real and
    active
    """
    return (
        db_session.query(DistrictTeacher)
        .filter(DistrictTeacher.employment_status.in_(['A', 'L']))
        .filter(DistrictTeacher.shared_teacher == False)
        .filter(DistrictTeacher.state_id_number != '')
    )

def staff_by_job_codes(job_codes):
    """
    Returns a query for staff with particular job codes
    """
    return (
        staff().filter(DistrictTeacher.job_roles.any(
            StaffJobRole.job_code.in_(job_codes)
        ))
    )

def teachers():
    """
    Returns a query of teachers
    Manually adds teachers who do not have SMIDs yet but should be setup with
    subscription services
    """
    extra_ids = []
    extra_query = (
        db_session.query(DistrictTeacher)
        .filter(DistrictTeacher.teacher_id.in_(extra_ids))
    )
    return staff_by_job_codes(teacher_job_codes).union(extra_query)

def admins():
    """
    Returns a query of ALL administrators
    """
    return staff_by_job_codes(
        principal_job_codes +
        supervisor_job_codes +
        other_admin_job_codes
    )

def sysadmins():
    """
    Returns a query of sysadmins.
    Manually adds Ed Tech Facilitator and Director of IT by ID
    """
    extra_ids = ['099', '9999', '947']
    extra_query = (
        db_session.query(DistrictTeacher)
        .filter(DistrictTeacher.teacher_id.in_(extra_ids))
    )

    return (
        staff_by_job_codes(sysadmin_job_codes).union(extra_query)
    )

def curradmins():
    """
    Returns a query of people who can edit ALL curriculum:
    * Supervisors
    * Assistant Superintendant
    * Curriculum Secretaries
    * Ed Tech facilitator
    """
    extra_ids = ['099', '7199', '947']
    extra_query = (
        db_session.query(DistrictTeacher)
        .filter(DistrictTeacher.teacher_id.in_(extra_ids))
    )

    return (
        staff_by_job_codes(supervisor_job_codes + ['0122'])
        .union(curriculum_secretaries())
        .union(extra_query)
    )

def edservices():
    """
    Returns a query of Educational Services staff.
    """
    return (
        staff_by_job_codes(edservices_job_codes)
    )

def nurses():
    """
    Returns a query of all the nurses.
    """
    return (
        staff_by_job_codes(nurse_job_codes)
    )

def fieldtrip_admins():
    """
    Returns a query of ALL people involved in the field trip approval process
    """
    extra_ids = [
        '5293', # AES
        '5139', # BBS
        '5211', # BES
        '5360', # Buildings and Grounds
        '269',  # Central Office
        '8114', # MTHS
        '5814', # MTMS
        '5158', # MLS
        '5156', # OTS
        '5251', # PPS
        '8167', # PPS
        '4950', # Transportation
        '5296', # WES
    ]
    extra_query = staff().filter(DistrictTeacher.teacher_id.in_(extra_ids))
    return nurses().union(extra_query)

# There is no difference in job code for the various types of secretaries so
# they must be specified by teacher_id
def principal_secretaries():
    return staff().filter(DistrictTeacher.teacher_id.in_([
        '5293', # AES
        '5139', # BBS
        '5211', # BES
        '5158', # MLS
        '5369', # MTHS
        '5156', # OTS
        '5297', # WLS
    ]))

def curriculum_secretaries():
    return staff().filter(DistrictTeacher.teacher_id.in_([
        '7199',
        '269',
        '5119',
    ]))

def hr_department():
    return staff().filter(DistrictTeacher.teacher_id.in_([
        '7144', # HR Director
        '6792', # Secretary: Employee AESOP / Certifications / Tuition Reimbursement
        '5390', # Secretary: Postings / Picture ID / New Hires
    ]))

def cert_staff():
    return staff().except_(staff_by_job_codes(noncert_job_codes))

def secretaries():
    return staff_by_job_codes(['9300'])

def media_staff():
    """
    Returns a query of ALL media center staff including Media Coordinators who
    are not certificated and DO NOT have a specific job code
    """
    extra_ids = [
        '7110', # MTMS Media Coordinator
    ]
    extra_query = staff().filter(DistrictTeacher.teacher_id.in_(extra_ids))
    return staff_by_job_codes(['3105', '3106']).union(extra_query)

def schools():
    """
    Returns a query of in-district schools
    """
    return (
        db_session.query(School)
        .filter(School.building_code.in_(school_codes))
    )

def courses():
    """
    Returns a query of active courses with sections that have at least one
    student in them in the current school year. DOES NOT include Homeroom
    courses
    """
    current_date = date.today()
    if current_date.month > 6: # Jul, Aug, Sep, Oct, Nov, Dec
        start_year = current_date.year
    else:                      # Jan, Feb, Mar, Apr, May, Jun
        start_year = current_date.year - 1
    ending = (start_year + 1) % 100 # last two digits of end_date
    school_year = f"{start_year}-{ending}"
    return (
        db_session.query(CurriculumCourse)
        .filter(CurriculumCourse.school_year == school_year)
        .filter(CurriculumCourse.course_code != '000')
        .filter(CurriculumCourse.course_active == True)
        .filter(CurriculumCourse.school_code.in_(school_codes))
        .filter(CurriculumCourse.sections.any(CourseSection.assigned_seats > 0))
    )

def sections():
    """
    Returns a query of active sections in all courses returned by courses()
    """
    return (
        courses()
        .join(CourseSection)
        .filter(CourseSection.assigned_seats > 0)
        .with_entities(CourseSection)
    )

def teacher_by_id(teacher_id):
    """
    Returns a DistrictTeacher object that matches a given teacher_id
    """
    return (
        db_session.query(DistrictTeacher)
        .filter(DistrictTeacher.teacher_id==teacher_id)
        .one()
    )

def teacher_by_name(first_name, last_name):
    """
    Returns the FIRST DistrictTeacher object that matches a given CASE
    INSENSITIVE first and last name
    """
    return (
        db_session.query(DistrictTeacher)
        .filter(func.lower(DistrictTeacher.teacher_first_name)==first_name.lower())
        .filter(func.lower(DistrictTeacher.teacher_last_name)==last_name.lower())
        .first()
    )

def student_by_id(student_id):
    """
    Returns a Student object that matches a given student_id
    """
    return (
        db_session.query(Student)
        .filter(Student.student_id==student_id)
        .one()
    )
