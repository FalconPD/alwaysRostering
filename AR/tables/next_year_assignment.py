from sqlalchemy import Column, String, Date, DateTime, Boolean, Integer
from sqlalchemy import BigInteger, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from AR.tables import Base, utils

class NextYearAssignment(Base):
    __tablename__ = 'NEXT_YEAR_ASSIGNMENTS'
    __table_args__ = (
        ForeignKeyConstraint(
            [
                'STUDENT_ID',
            ],
            [
                'STUDENTS.STUDENT_ID',
            ]
        ),
    )

    counselor_id = Column('COUNSELOR_ID', String(10))
    created_by_portal_oid = Column('CREATED_BY_PORTAL_OID', BigInteger)
    created_by_task_oid = Column('CREATED_BY_TASK_OID', BigInteger)
    created_by_user_oid = Column('CREATED_BY_USER_OID', BigInteger)
    created_ip = Column('CREATED_IP', String(100))
    created_on = Column('CREATED_ON', DateTime)
    drop_from_scheduling  = Column('DROP_FROM_SCHEDULING', Boolean, nullable=False)
    entry_code = Column('ENTRY_CODE', String(3))
    gradeLevel = Column('GRADE_LEVEL', String(3))
    homeroom = Column('HOMEROOM', String(25))
    last_updated_by_portal_oid = Column('LAST_UPDATED_BY_PORTAL_OID', BigInteger)
    last_updated_by_task_oid = Column('LAST_UPDATED_BY_TASK_OID', BigInteger)
    last_updated_by_user_oid = Column('LAST_UPDATED_BY_USER_OID', BigInteger)
    last_updated_ip = Column('LAST_UPDATED_IP', String(100))
    last_updated = Column('LAST_UPDATED', DateTime)
    note = Column('NOTE', String)
    pre_instruction_day1_withdraw_code = Column('PRE_DAY1_WITHDRAW_CODE', String(50))
    pre_instruction_day1_withdraw_school = Column('PRE_DAY1_WITHDRAW_SCHOOL', String(50))
    pre_instruction_day2_entry_code = Column('PRE_DAY2_ENTRY_CODE', String(50))
    program_type_code = Column('PROGRAM_TYPE_CODE', String(8))
    promote = Column('PROMOTE', Boolean, nullable=False)
    schedule_locked = Column('SCHEDULE_LOCKED', Boolean, nullable=False)
    scheduling_group = Column('SCHEDULING_GROUP', String(5))                   
    scheduling_priority = Column('SCHEDULING_PRIORITY', Integer)
    school_code = Column('SCHOOL_CODE', String(8), nullable=False)
    school_code_set_by_school_mint = Column('SCHOOL_CODE_SET_BY_SCHOOLMINT', Boolean, nullable=False)
    school_year = Column('SCHOOL_YEAR', String(7), nullable=False, primary_key=True)
    session = Column('SESSION_CODE', String(2))
    student_id = Column('STUDENT_ID', String(15), nullable=False, primary_key=True)
    team_code = Column('TEAM_CODE', String(8))
    transferred_to_county = Column('TRANS_COUNTY', String(2))
    transferred_to_district = Column('TRANS_DISTRICT', String(9))
    transferred_to_first_day_attendance = Column('TRANS_FIRST_ATTENDANCE_DATE', Date) 
    transferred_to_school = Column('TRANS_SCHOOL', String(4)) 
    withdrawal_reason_code = Column('REASON_CODE', String(50))

    student = relationship('Student', back_populates='next_year_assignment')

    report_code = '991193'
    csv_header = [ 
        'COUNSELOR_ID',
        'CREATED_BY_PORTAL_OID',
        'CREATED_BY_TASK_OID',
        'CREATED_BY_USER_OID',
        'CREATED_IP',
        'CREATED_ON',
        'DROP_FROM_SCHEDULING',
        'ENTRY_CODE',
        'GRADE_LEVEL',
        'HOMEROOM',
        'LAST_UPDATED_BY_PORTAL_OID',
        'LAST_UPDATED_BY_TASK_OID',
        'LAST_UPDATED_BY_USER_OID',
        'LAST_UPDATED_IP',
        'LAST_UPDATED',
        'NOTE',
        'PRE_DAY1_WITHDRAW_CODE',
        'PRE_DAY1_WITHDRAW_SCHOOL',
        'PRE_DAY2_ENTRY_CODE',
        'PROGRAM_TYPE_CODE',
        'PROMOTE',
        'SCHEDULE_LOCKED',
        'SCHEDULING_GROUP',
        'SCHEDULING_PRIORITY',
        'SCHOOL_CODE',
        'SCHOOL_CODE_SET_BY_SCHOOLMINT',
        'SCHOOL_YEAR',
        'SESSION_CODE',
        'STUDENT_ID',
        'TEAM_CODE',
        'TRANS_COUNTY',
        'TRANS_DISTRICT',
        'TRANS_FIRST_ATTENDANCE_DATE',
        'TRANS_SCHOOL',
        'REASON_CODE',
    ]

    @classmethod
    def from_csv(cls, row):
        return cls(
            counselor_id                         = row[0],
            created_by_portal_oid                = row[1],
            created_by_task_oid                  = row[2],
            created_by_user_oid                  = row[3],
            created_ip                           = row[4],
            created_on                           = utils.genesis_to_datetime(row[5]),
            drop_from_scheduling                 = utils.genesis_to_boolean(row[6]),
            entry_code                           = row[7],
            gradeLevel                           = row[8],
            homeroom                             = row[9],
            last_updated_by_portal_oid           = row[10],
            last_updated_by_task_oid             = row[11],
            last_updated_by_user_oid             = row[12],
            last_updated_ip                      = row[13],
            last_updated                         = utils.genesis_to_datetime(row[14]),
            note                                 = row[15],
            pre_instruction_day1_withdraw_code   = row[16],
            pre_instruction_day1_withdraw_school = row[17],
            pre_instruction_day2_entry_code      = row[18],
            program_type_code                    = row[19],
            promote                              = utils.genesis_to_boolean(row[20]),
            schedule_locked                      = utils.genesis_to_boolean(row[21]),
            scheduling_group                     = row[22],
            scheduling_priority                  = row[23],
            school_code                          = row[24],
            school_code_set_by_school_mint       = utils.genesis_to_boolean(row[25]),
            school_year                          = row[26],
            session                              = row[27],
            student_id                           = row[28],
            team_code                            = row[29],
            transferred_to_county                = row[30],
            transferred_to_district              = row[31],
            transferred_to_first_day_attendance  = utils.genesis_to_date(row[32]),
            transferred_to_school                = row[33],
            withdrawal_reason_code               = row[34],
        )

    def __repr__(self):
        return (
                f"NextYearAssignment student_id={student_id} "
                f"school_year={school_year} school_code={school_code}"
            )
