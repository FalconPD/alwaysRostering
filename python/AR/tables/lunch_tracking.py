from sqlalchemy import Column, BigInteger, Boolean, Date, DateTime, String
from AR.tables import utils, Base

class LunchTrackingRecord(Base):
    __tablename__ = 'LUNCH_TRACKING'

    carry_over_record = Column('CARRY_OVER', Boolean, nullable=False)
    created_by_portal_oid = Column('CREATED_BY_PORTAL_OID', BigInteger)    
    created_by_task_oid = Column('CREATED_BY_TASK_OID', BigInteger)    
    created_by_user_oid = Column('CREATED_BY_USER_OID', BigInteger)    
    created_ip = Column('CREATED_IP', String(100))    
    created_on = Column('CREATED_ON', DateTime)
    elig_letter_printed = Column('ELIG_LETTER_PRINTED', Date)
    end_date = Column('END_DATE', Date)
    last_updated_by_portal_oid = Column('LAST_UPDATED_BY_PORTAL_OID', BigInteger)
    last_updated_by_task_oid = Column('LAST_UPDATED_BY_TASK_OID', BigInteger)
    last_updated_by_user_oid = Column('LAST_UPDATED_BY_USER_OID', BigInteger)
    last_updated_ip = Column('LAST_UPDATED_IP', String(100))
    last_updated = Column('LAST_UPDATED', DateTime)
    lunch_code = Column('LUNCH_CODE', String, nullable=False)
    objectid = Column('OBJECT_ID', BigInteger, primary_key=True)
    school_year = Column('SCHOOL_YEAR', String, nullable=False)
    start_date = Column('START_DATE', Date, nullable=False)
    student_id = Column('STUDENT_ID', String, nullable=False)

    report_code = '991182'
    csv_header = [
        'CARRY_OVER',
        'CREATED_BY_PORTAL_OID',
        'CREATED_BY_TASK_OID',
        'CREATED_BY_USER_OID',
        'CREATED_IP',
        'CREATED_ON',
        'ELIG_LETTER_PRINTED',
        'END_DATE',
        'LAST_UPDATED_BY_PORTAL_OID',
        'LAST_UPDATED_BY_TASK_OID',
        'LAST_UPDATED_BY_USER_OID',
        'LAST_UPDATED_IP',
        'LAST_UPDATED',
        'LUNCH_CODE',
        'OBJECT_ID',
        'SCHOOL_YEAR',
        'START_DATE',
        'STUDENT_ID',
    ]

    @classmethod
    def from_csv(cls, row):
        return cls(
            carry_over_record          = utils.genesis_to_boolean(row[0]),
            created_by_portal_oid      = row[1],
            created_by_task_oid        = row[2],
            created_by_user_oid        = row[3],
            created_ip                 = row[4],
            created_on                 = utils.genesis_to_datetime(row[5]),
            elig_letter_printed        = utils.genesis_to_date(row[6]),
            end_date                   = utils.genesis_to_date(row[7]),
            last_updated_by_portal_oid = row[8],
            last_updated_by_task_oid   = row[9],
            last_updated_by_user_oid   = row[10],
            last_updated_ip            = row[11],
            last_updated               = utils.genesis_to_datetime(row[12]),
            lunch_code                 = row[13],
            objectid                   = row[14],
            school_year                = row[15],
            start_date                 = utils.genesis_to_date(row[16]),
            student_id                 = row[17],
        )

    def __repr__(self):
        return (
            f"LunchTrackingRecord school_year={self.school_year} "
            f"student_id={self.student_id} lunch_code={self.lunch_code} "
            f"start_date={self.start_date} end_date={self.end_date}"
        )
