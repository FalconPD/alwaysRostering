from sqlalchemy import Column, Integer, String, Boolean, BigInteger, DateTime
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy.orm import relationship
from AR.tables import Base
from AR.tables import utils

class SchoolTeacher(Base):
    __tablename__ = 'SCHOOL_TEACHERS'
    __table_args__ = (
        ForeignKeyConstraint(
            [
                'CURRENT_HOMEROOM',
                'SCHOOL_CODE',
                'SCHOOL_YEAR',
            ],
            [
                'STUDENTS.HOMEROOM',
                'STUDENTS.CURRENT_SCHOOL',
                'STUDENTS.SCHOOL_YEAR',
            ],
        ),
        ForeignKeyConstraint(
            [
                'SCHOOL_YEAR',
                'TEACHER_ID',
            ],
            [
                'DISTRICT_TEACHERS.SCHOOL_YEAR',
                'DISTRICT_TEACHERS.TEACHER_ID',
            ],
        ),
    )

    attendance_homeroom = Column('ATTENDANCE_HOMEROOM', String(25))
    basic_skills_teacher = Column('BASIC_SKILLS_TEACHER', Boolean,
        nullable=False)
    created_by_portal_oid = Column('CREATED_BY_PORTAL_OID', BigInteger)
    created_by_task_oid = Column('CREATED_BY_TASK_OID', BigInteger)
    created_by_user_oid = Column('CREATED_BY_USER_OID', BigInteger)
    created_ip = Column('CREATED_IP', String(100))
    created_on = Column('CREATED_ON', DateTime)
    current_homeroom = Column('CURRENT_HOMEROOM', String(25))
    department_code = Column('DEPARTMENT_CODE', String(8))
    department_head = Column('DEPARTMENT_HEAD', Boolean, nullable=False)
    elem_comment_seq = Column('ELEM_COMMENT_SEQ', Integer, nullable=False)
    builder_does_not_req_lunch = Column('BUILDER_DOES_NOT_REQ_LUNCH', Boolean, nullable=False)
    grade_level = Column('GRADE_LEVEL', String(3))
    last_updated_by_portal_oid = Column('LAST_UPDATED_BY_PORTAL_OID', BigInteger)
    last_updated_by_task_oid = Column('LAST_UPDATED_BY_TASK_OID', BigInteger)
    last_updated_by_user_oid = Column('LAST_UPDATED_BY_USER_OID', BigInteger)
    last_updated_ip = Column('LAST_UPDATED_IP', String(100))
    last_updated = Column('LAST_UPDATED', DateTime)
    mail_location_code = Column('MAIL_LOCATION_CODE', String(8))
    max_periods_day = Column('MAX_PERIODS_DAY', Integer)
    max_seq_periods = Column('MAX_SEQ_PERIODS', Integer)
    max_students_in_class = Column('MAX_STUDENTS_IN_CLASS', Integer)
    max_students_per_day = Column('MAX_STUDENTS_PER_DAY', Integer)
    min_periods_day = Column('MIN_PERIODS_DAY', Integer)
    next_homeroom = Column('NEXT_HOMEROOM', String(25))
    percent_of_time_in_school = Column('PERCENT_OF_TIME_IN_SCHOOL', Integer)
    preferred_room = Column('PREFERRED_ROOM', String(25))
    primary_school_assignment = Column('PRIMARY_SCHOOL_ASSIGNMENT', Boolean, nullable=False)
    school_code = Column('SCHOOL_CODE', String(8), nullable=False, primary_key=True)
    school_year = Column('SCHOOL_YEAR', String(7), nullable=False, primary_key=True)
    teacher_seq = Column('TEACHER_SEQ', Integer, nullable=False)
    sif_id = Column('SIF_ID', String(32))
    special_subject_teacher = Column('SPECIAL_SUBJECT_TEACHER', Boolean, nullable=False)
    teacher_id = Column('TEACHER_ID', String(10), nullable=False, primary_key=True)
    team_code = Column('TEAM_CODE', String(8))

    homeroom_students = relationship('Student',
        back_populates='homeroom_school_teacher', viewonly=True)
    district_teacher = relationship('DistrictTeacher',
        back_populates='school_teacher', viewonly=True)

    report_code = '991021'
    csv_header = [
        'ATTENDANCE_HOMEROOM',
        'BASIC_SKILLS_TEACHER',
        'CREATED_BY_PORTAL_OID',
        'CREATED_BY_TASK_OID',
        'CREATED_BY_USER_OID',
        'CREATED_IP',
        'CREATED_ON',
        'CURRENT_HOMEROOM',
        'DEPARTMENT_CODE',
        'DEPARTMENT_HEAD',
        'ELEM_COMMENT_SEQ',
        'BUILDER_DOES_NOT_REQ_LUNCH',
        'GRADE_LEVEL',
        'LAST_UPDATED_BY_PORTAL_OID',
        'LAST_UPDATED_BY_TASK_OID',
        'LAST_UPDATED_BY_USER_OID',
        'LAST_UPDATED_IP',
        'LAST_UPDATED',
        'MAIL_LOCATION_CODE',
        'MAX_PERIODS_DAY',
        'MAX_SEQ_PERIODS',
        'MAX_STUDENTS_IN_CLASS',
        'MAX_STUDENTS_PER_DAY',
        'MIN_PERIODS_DAY',
        'NEXT_HOMEROOM',
        'PERCENT_OF_TIME_IN_SCHOOL',
        'PREFERRED_ROOM',
        'PRIMARY_SCHOOL_ASSIGNMENT',
        'SCHOOL_CODE',
        'SCHOOL_YEAR',
        'TEACHER_SEQ',
        'SIF_ID',
        'SPECIAL_SUBJECT_TEACHER',
        'TEACHER_ID',
        'TEAM_CODE'
    ]

    @classmethod
    def from_csv(cls, row):
        return cls(
            attendance_homeroom         = row[0],
            basic_skills_teacher        = utils.genesis_to_boolean(row[1]),
            created_by_portal_oid       = row[2],
            created_by_task_oid         = row[3],
            created_by_user_oid         = row[4],
            created_ip                  = row[5],
            created_on                  = utils.genesis_to_datetime(row[6]),
            current_homeroom            = row[7],
            department_code             = row[8],
            department_head             = utils.genesis_to_boolean(row[9]),
            elem_comment_seq            = row[10],
            builder_does_not_req_lunch  = utils.genesis_to_boolean(row[11]),
            grade_level                 = row[12],
            last_updated_by_portal_oid  = row[13],
            last_updated_by_task_oid    = row[14],
            last_updated_by_user_oid    = row[15],
            last_updated_ip             = row[16],
            last_updated                = utils.genesis_to_datetime(row[17]),
            mail_location_code          = row[18],
            max_periods_day             = row[19],
            max_seq_periods             = row[20],
            max_students_in_class       = row[21],
            max_students_per_day        = row[22],
            min_periods_day             = row[23],
            next_homeroom               = row[24],
            percent_of_time_in_school   = row[25],
            preferred_room              = row[26],
            primary_school_assignment   = utils.genesis_to_boolean(row[27]),
            school_code                 = row[28],
            school_year                 = row[29],
            teacher_seq                 = row[30],
            sif_id                      = row[31],
            special_subject_teacher     = utils.genesis_to_boolean(row[32]),
            teacher_id                  = row[33],
            team_code                   = row[34]
        )

    def __repr__(self):
        return "SchoolTeacher teacher_id={} school_code={}".format(
            self.teacher_id, self.school_code)
