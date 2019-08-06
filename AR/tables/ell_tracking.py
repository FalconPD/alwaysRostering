from sqlalchemy import Column, BigInteger, Boolean, Date, DateTime, String
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy.orm import relationship
from AR.tables import utils, Base

class ELLTracking(Base):
    __tablename__ = 'ELL_TRACKING'
    __table_args__ = (
        ForeignKeyConstraint(
            [
                'STUDENT_ID',
            ],
            [
                'STUDENTS.STUDENT_ID',
            ],
        ),
    )

    created_by_portal_oid = Column('CREATED_BY_PORTAL_OID', BigInteger)
    created_by_task_oid = Column('CREATED_BY_TASK_OID', BigInteger)
    created_by_user_oid = Column('CREATED_BY_USER_OID', BigInteger)        
    created_ip = Column('CREATED_IP', String(100))
    created_on = Column('CREATED_ON', DateTime)
    exit_date = Column('EXIT_DATE', Date)
    exit_reason = Column('EXIT_REASON', String(100))
    initial_eligibility = Column('INITIAL_ELIGIBILITY', String(25))
    last_updated_by_portal_oid = Column('LAST_UPDATED_BY_PORTAL_OID', BigInteger)
    last_updated_by_task_oid = Column('LAST_UPDATED_BY_TASK_OID', BigInteger)
    last_updated_by_user_oid = Column('LAST_UPDATED_BY_USER_OID', BigInteger)
    last_updated_ip = Column('LAST_UPDATED_IP', String(100))
    last_updated_on = Column('LAST_UPDATED_ON', DateTime)
    notes = Column('NOTES', String(2048))
    objectid = Column('OBJECT_ID', BigInteger, nullable=False, primary_key=True)
    participation_code = Column('PARTICIPATION_CODE', String(8))
    program_start_date = Column('PROGRAM_START_DATE', Date)
    program_type = Column('PROGRAM_TYPE', String(50))
    referral_date = Column('REFERRAL_DATE', Date)
    start_date = Column('START_DATE', Date)
    student_id = Column('STUDENT_ID', String(15), nullable=False)

    student = relationship('Student', back_populates='ell_tracking')

    report_code = '991186'
    csv_header = [
        'CREATED_BY_PORTAL_OID',
        'CREATED_BY_TASK_OID',
        'CREATED_BY_USER_OID',
        'CREATED_IP',
        'CREATED_ON',
        'EXIT_DATE',
        'EXIT_REASON',
        'INITIAL_ELIGIBILITY',
        'LAST_UPDATED_BY_PORTAL_OID',
        'LAST_UPDATED_BY_TASK_OID',
        'LAST_UPDATED_BY_USER_OID',
        'LAST_UPDATED_IP',
        'LAST_UPDATED_ON',
        'NOTES',
        'OBJECT_ID',
        'PARTICIPATION_CODE',
        'PROGRAM_START_DATE',
        'PROGRAM_TYPE',
        'REFERRAL_DATE',
        'START_DATE',
        'STUDENT_ID',
    ]

    @classmethod
    def from_csv(cls, row):
        return cls(
            created_by_portal_oid = row[0],
            created_by_task_oid = row[1],
            created_by_user_oid = row[2],
            created_ip = row[3],
            created_on = utils.genesis_to_datetime(row[4]),
            exit_date = utils.genesis_to_date(row[5]),
            exit_reason = row[6],
            initial_eligibility = row[7],
            last_updated_by_portal_oid = row[8],
            last_updated_by_task_oid = row[9],
            last_updated_by_user_oid = row[10],
            last_updated_ip = row[11],
            last_updated_on = utils.genesis_to_datetime(row[12]),
            notes = row[13],
            objectid = row[14],
            participation_code = row[15],
            program_start_date = utils.genesis_to_date(row[16]),
            program_type = row[17],
            referral_date = utils.genesis_to_date(row[18]),
            start_date = utils.genesis_to_date(row[19]),
            student_id = row[20],
        )

    def __repr__(self):
        return (
            f"ELLTracking student_id={self.student_id} "
            f"program_type={self.program_type} start_date={self.start_date} "
            f"exit_date={self.exit_date}"
        )
