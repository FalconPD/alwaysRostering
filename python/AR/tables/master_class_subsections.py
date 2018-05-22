from sqlalchemy import Column, Integer, String, Boolean, BigInteger, DateTime, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from AR.tables import Base
from AR.tables import utils

class CourseSubsection(Base):
    __tablename__ = 'MASTER_CLASS_SUBSECTIONS'
    __table_args__ = (
        ForeignKeyConstraint(['SCHOOL_YEAR', 'SCHOOL_CODE','COURSE_CODE', 'COURSE_SECTION'],
            ['MASTER_CLASS_SCHEDULE.SCHOOL_YEAR', 'MASTER_CLASS_SCHEDULE.SCHOOL_CODE',
            'MASTER_CLASS_SCHEDULE.COURSE_CODE', 'MASTER_CLASS_SCHEDULE.COURSE_SECTION']),
    )

    alternate_bell_code = Column('ALTERNATE_BELL_CODE', String(7))
    course_code = Column('COURSE_CODE', String(25), primary_key=True, nullable=False)
    course_section = Column('COURSE_SECTION', Integer, primary_key=True, nullable=False)
    created_by_portal_oid = Column('CREATED_BY_PORTAL_OID', BigInteger)
    created_by_task_oid = Column('CREATED_BY_TASK_OID', BigInteger)
    created_by_user_oid = Column('CREATED_BY_USER_OID', BigInteger)
    created_ip = Column('CREATED_IP', String(100))
    created_on = Column('CREATED_ON', DateTime)
    exclued_njsmart = Column('EXCLUDE_NJSMART', Boolean, nullable=False)
    from_period = Column('FROM_PERIOD', Integer, nullable=False)
    include_teacher_in_printing = Column('INCLUDE_TEACHER_IN_PRINTING', Boolean, nullable=False)
    last_updated_by_portal_oid = Column('LAST_UPDATED_BY_PORTAL_OID', BigInteger)
    last_updated_by_task_oid = Column('LAST_UPDATED_BY_TASK_OID', BigInteger)
    last_updated_by_user_oid = Column('LAST_UPDATED_BY_USER_OID', BigInteger)
    last_updated_ip = Column('LAST_UPDATED_IP', String(100))
    last_updated = Column('LAST_UPDATED', DateTime)
    meets_cycles = Column('MEETS_CYCLES', String(15), nullable=False)
    print_period = Column('PRINT_PERIOD', String(5))
    report_card_teacher_id = Column('REPORT_CARD_TEACHER_ID', String(10))
    room_number = Column('ROOM_NUMBER', String(25))
    school_code = Column('SCHOOL_CODE', String(8), primary_key=True, nullable=False)
    school_year = Column('SCHOOL_YEAR', String(7), primary_key=True, nullable=False)
    semester = Column('SEMESTER', String(3), nullable=False)
    subsection = Column('SUBSECTION', Integer, primary_key=True, nullable=False)
    subsection_description = Column('SUBSECTION_DESCRIPTION', String(50))
    teacher_id = Column('TEACHER_ID', String(10))
    thru_period = Column('THRU_PERIOD', Integer, nullable=False)

    section = relationship('CourseSection', back_populates='subsections')

    report_code = '991074'
    csv_header = [ 
        'ALTERNATE_BELL_CODE',
        'COURSE_CODE',
        'COURSE_SECTION',
        'CREATED_BY_PORTAL_OID',
        'CREATED_BY_TASK_OID',
        'CREATED_BY_USER_OID',
        'CREATED_IP',
        'CREATED_ON',
        'EXCLUDE_NJSMART',
        'FROM_PERIOD',
        'INCLUDE_TEACHER_IN_PRINTING',
        'LAST_UPDATED_BY_PORTAL_OID',
        'LAST_UPDATED_BY_TASK_OID',
        'LAST_UPDATED_BY_USER_OID',
        'LAST_UPDATED_IP',
        'LAST_UPDATED',
        'MEETS_CYCLES',
        'PRINT_PERIOD',
        'REPORT_CARD_TEACHER_ID',
        'ROOM_NUMBER',
        'SCHOOL_CODE',
        'SCHOOL_YEAR',
        'SEMESTER',
        'SUBSECTION',
        'SUBSECTION_DESCRIPTION',
        'TEACHER_ID',
        'THRU_PERIOD'
    ]

    @classmethod
    def from_csv(cls, row):
        return cls(
            alternate_bell_code             = row[0],
            course_code                     = row[1],
            course_section                  = row[2],
            created_by_portal_oid           = row[3],
            created_by_task_oid             = row[4],
            created_by_user_oid             = row[5],
            created_ip                      = row[6],
            created_on                      = utils.genesis_to_datetime(row[7]),
            exclued_njsmart                 = utils.genesis_to_boolean(row[8]),
            from_period                     = row[9],
            include_teacher_in_printing     = utils.genesis_to_boolean(row[10]),
            last_updated_by_portal_oid      = row[11],
            last_updated_by_task_oid        = row[12],
            last_updated_by_user_oid        = row[13],
            last_updated_ip                 = row[14],
            last_updated                    = utils.genesis_to_datetime(row[15]),
            meets_cycles                    = row[16],
            print_period                    = row[17],
            report_card_teacher_id          = row[18],
            room_number                     = row[19],
            school_code                     = row[20],
            school_year                     = row[21],
            semester                        = row[22],
            subsection                      = row[23],
            subsection_description          = row[24],
            teacher_id                      = row[25],
            thru_period                     = row[26]
        )

    def __repr__(self):
        return (
                "CourseSubsection "
                "school_code={} "
                "course_code={} "
                "course_section={} "
                "subsection={} "
                "subsection_description={}"
            ).format(
                self.school_code,
                self.course_code,
                self.course_section,
                self.subsection,
                self.subsection_description
            )
