from sqlalchemy import Column, Integer, String, Boolean, BigInteger, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from AR.tables import Base
from AR.tables import utils

class StudentSchedule(Base):
    __tablename__ = 'STUDENT_SCHEDULE'

    course_code = Column('COURSE_CODE', String(25), nullable=False, primary_key=True)
    course_section = Column('COURSE_SECTION', Integer, nullable=False, primary_key=True)
    course_status = Column('COURSE_STATUS', String(8))
    course_status_date = Column('COURSE_STATUS_DATE', Date, nullable=False)
    created_by_portal_oid = Column('CREATED_BY_PORTAL_OID', BigInteger)
    created_by_task_oid = Column('CREATED_BY_TASK_OID', BigInteger)
    created_by_user_oid = Column('CREATED_BY_USER_OID', BigInteger)
    created_ip = Column('CREATED_IP', String(100))
    created_on = Column('CREATED_ON', DateTime)
    last_updated = Column('LAST_UPDATED', DateTime)
    last_updated_by_portal_oid = Column('LAST_UPDATED_BY_PORTAL_OID', BigInteger)
    last_updated_by_task_oid = Column('LAST_UPDATED_BY_TASK_OID', BigInteger)
    last_updated_by_user_oid = Column('LAST_UPDATED_BY_USER_OID', BigInteger)
    last_updated_ip = Column('LAST_UPDATED_IP', String(100))
    not_dual_credit = Column('NOT_DUAL_CREDIT', Boolean, nullable=False)
    scheduling_run_code = Column('SCHEDULING_RUN_CODE', String(50))
    scheme_code = Column('SCHEME_CODE', String(15))
    scheme_locked = Column('SCHEME_LOCKED', Boolean, nullable=False)
    school_code = Column('SCHOOL_CODE', String(8), nullable=False, primary_key=True)
    school_year = Column('SCHOOL_YEAR', String(7), nullable=False, primary_key=True)
    sifid = Column('SIFID', String(32))
    student_exit_date = Column('STUDENT_EXIT_DATE', Date)
    student_id = Column('STUDENT_ID', String(15), ForeignKey('STUDENTS.STUDENT_ID'), nullable=False, primary_key=True)
    student_start_date = Column('STUDENT_START_DATE', Date)
    use_in_student_sel_gpa = Column('USE_IN_STUDENT_SEL_GPA', Boolean, nullable=False)
    userid = Column('USERID', String(100))

    student = relationship('Student', back_populates='student_schedule')

    report_code = '991015'
    csv_header = [
        'COURSE_CODE',
        'COURSE_SECTION',
        'COURSE_STATUS',
        'COURSE_STATUS_DATE',
        'CREATED_BY_PORTAL_OID',
        'CREATED_BY_TASK_OID',
        'CREATED_BY_USER_OID',
        'CREATED_IP',
        'CREATED_ON',
        'LAST_UPDATED',
        'LAST_UPDATED_BY_PORTAL_OID',
        'LAST_UPDATED_BY_TASK_OID',
        'LAST_UPDATED_BY_USER_OID',
        'LAST_UPDATED_IP',
        'NOT_DUAL_CREDIT',
        'SCHEDULING_RUN_CODE',
        'SCHEME_CODE',
        'SCHEME_LOCKED',
        'SCHOOL_CODE',
        'SCHOOL_YEAR',
        'SIFID',
        'STUDENT_EXIT_DATE',
        'STUDENT_ID',
        'STUDENT_START_DATE',
        'USE_IN_STUDENT_SEL_GPA',
        'USERID'
    ]

    @classmethod
    def from_csv(cls, row):
        return cls(
            course_code                = row[0],
            course_section             = row[1],
            course_status              = row[2],
            course_status_date         = utils.genesis_to_date(row[3]),
            created_by_portal_oid      = row[4],
            created_by_task_oid        = row[5],
            created_by_user_oid        = row[6],
            created_ip                 = row[7],
            created_on                 = utils.genesis_to_datetime(row[8]),
            last_updated               = utils.genesis_to_datetime(row[9]),
            last_updated_by_portal_oid = row[10],
            last_updated_by_task_oid   = row[11],
            last_updated_by_user_oid   = row[12],
            last_updated_ip            = row[13],
            not_dual_credit            = utils.genesis_to_boolean(row[14]),
            scheduling_run_code        = row[15],
            scheme_code                = row[16],
            scheme_locked              = utils.genesis_to_boolean(row[17]),
            school_code                = row[18],
            school_year                = row[19],
            sifid                      = row[20],
            student_exit_date          = utils.genesis_to_date(row[21]),
            student_id                 = row[22],
            student_start_date         = utils.genesis_to_date(row[23]),
            use_in_student_sel_gpa     = utils.genesis_to_boolean(row[24]),
            userid                     = row[25]
        )

    def __repr__(self):
        return "<StudentSchedule(student_id={}, course_code={}, course_section={})>".format(self.student_id, self.course_code, self.course_section) 
