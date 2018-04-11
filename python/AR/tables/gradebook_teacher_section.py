from sqlalchemy import Column, Integer, String, Boolean, BigInteger, DateTime, orm
from AR.tables import Base
from AR.tables import utils

class GradebookTeacherSection(Base):
    __tablename__ = 'GRADEBOOK_TEACHER_SECTIONS2'
    active = Column('ACTIVE', Boolean, nullable=False)
    course_code = Column('COURSE_CODE', String(25), nullable=False, primary_key=True)
    course_id = Column('COURSE_ID', BigInteger, nullable=False)
    course_section = Column('COURSE_SECTION', Integer, nullable=False, primary_key=True)
    created_by_portal_oid = Column('CREATED_BY_PORTAL_OID', BigInteger)
    created_by_task_oid = Column('CREATED_BY_TASK_OID', BigInteger)
    created_by_user_oid = Column('CREATED_BY_USER_OID', BigInteger)
    created_ip = Column('CREATED_IP', String(100))
    created_on = Column('CREATED_ON', DateTime)
    default_set_code = Column('DEFAULT_SET_CODE', String(20))
    default_subject_code = Column('DEFAULT_SUBJECT_CODE', String(20))
    department_code = Column('DEPARTMENT_CODE', String(50))
    description = Column('DESCRIPTION', String(255), nullable=False)
    gb_description = Column('GB_DESCRIPTION', String(255), nullable=False)
    hide_gradebook = Column('HIDE_GRADEBOOK', Boolean, nullable=False)
    last_accessed = Column('LAST_ACCESSED', DateTime)
    last_accessed_by = Column('LAST_ACCESSED_BY', String(100))
    last_updated_by_portal_oid = Column('LAST_UPDATED_BY_PORTAL_OID', BigInteger)
    last_updated_by_task_oid = Column('LAST_UPDATED_BY_TASK_OID', BigInteger)
    last_updated_by_user_oid = Column('LAST_UPDATED_BY_USER_OID', BigInteger)
    last_updated_ip = Column('LAST_UPDATED_IP', String(100))
    last_updated = Column('LAST_UPDATED', DateTime)
    locked_mp_grades = Column('LOCKED_MP_GRADES', String(50))
    meets_cycles = Column('MEETS_CYCLES', String(20))
    merged = Column('MERGED', Boolean, nullable=False)
    merged_by = Column('MERGED_BY', String(100))
    merged_date = Column('MERGED_DATE', DateTime)
    print_periods = Column('PRINT_PERIODS', String(50))
    profile_code = Column('PROFILE_CODE', String(8), nullable=False)
    rooms = Column('ROOMS', String(100))
    school_code = Column('SCHOOL_CODE', String(8), nullable=False, primary_key=True)
    school_year = Column('SCHOOL_YEAR', String(7), nullable=False, primary_key=True)
    semester = Column('SEMESTER', String(3), nullable=False)
    seq = Column('SEQ', Integer, nullable=False)
    teacher_id = Column('TEACHER_ID', String(10), nullable=False, primary_key=True)

    report_code = '991022'
    csv_header = [
        'ACTIVE',
        'COURSE_CODE',
        'COURSE_ID',
        'COURSE_SECTION',
        'CREATED_BY_PORTAL_OID',
        'CREATED_BY_TASK_OID',
        'CREATED_BY_USER_OID',
        'CREATED_IP',
        'CREATED_ON',
        'DEFAULT_SET_CODE',
        'DEFAULT_SUBJECT_CODE',
        'DEPARTMENT_CODE',
        'DESCRIPTION',
        'GB_DESCRIPTION',
        'HIDE_GRADEBOOK',
        'LAST_ACCESSED',
        'LAST_ACCESSED_BY',
        'LAST_UPDATED_BY_PORTAL_OID',
        'LAST_UPDATED_BY_TASK_OID',
        'LAST_UPDATED_BY_USER_OID',
        'LAST_UPDATED_IP',
        'LAST_UPDATED',
        'LOCKED_MP_GRADES',
        'MEETS_CYCLES',
        'MERGED',
        'MERGED_BY',
        'MERGED_DATE',
        'PRINT_PERIODS',
        'PROFILE_CODE',
        'ROOMS',
        'SCHOOL_CODE',
        'SCHOOL_YEAR',
        'SEMESTER',
        'SEQ',
        'TEACHER_ID'
    ]

    @classmethod
    def from_csv(cls, row):
        return cls(
            active                      = utils.genesis_to_boolean(row[0]),
            course_code                 = row[1],
            course_id                   = row[2],
            course_section              = row[3],
            created_by_portal_oid       = row[4],
            created_by_task_oid         = row[5],
            created_by_user_oid         = row[6],
            created_ip                  = row[7],
            created_on                  = utils.genesis_to_datetime(row[8]),
            default_set_code            = row[9],
            default_subject_code        = row[10],
            department_code             = row[11],
            description                 = row[12],
            gb_description              = row[13],
            hide_gradebook              = utils.genesis_to_boolean(row[14]),
            last_accessed               = utils.genesis_to_datetime(row[15]),
            last_accessed_by            = row[16],
            last_updated_by_portal_oid  = row[17],
            last_updated_by_task_oid    = row[18],
            last_updated_by_user_oid    = row[19],
            last_updated_ip             = row[20],
            last_updated                = utils.genesis_to_datetime(row[21]),
            locked_mp_grades            = row[22],
            meets_cycles                = row[23],
            merged                      = utils.genesis_to_boolean(row[24]),
            merged_by                   = row[25],
            merged_date                 = utils.genesis_to_datetime(row[26]),
            print_periods               = row[27],
            profile_code                = row[28],
            rooms                       = row[29],
            school_code                 = row[30],
            school_year                 = row[31],
            semester                    = row[32],
            seq                         = row[33],
            teacher_id                  = row[34]
        )
