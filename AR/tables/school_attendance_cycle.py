from sqlalchemy import Column, String, Boolean, BigInteger, Date, DateTime
from sqlalchemy import Integer 
from AR.tables import Base
from AR.tables import utils

class SchoolAttendanceCycle(Base):
    __tablename__ = 'SCHOOL_ATTENDANCE_CYCLES'

    school_year = Column('SCHOOL_YEAR', String(7), nullable=False, primary_key=True)
    school_code = Column('SCHOOL_CODE', String (8), nullable=False, primary_key=True)
    code = Column('ATTENDANCE_CYCLE_CODE', String(15), nullable=False, primary_key=True)
    description = Column('ATTENDANCE_CYCLE_DESCRIPTION', String(50), nullable=False)                  
    end_date = Column('ATTENDANCE_CYCLE_END_DATE', Date, nullable=False)
    gb_description = Column('GB_DESCRIPTION', String(5))
    read_only = Column('READ_ONLY', Boolean, nullable=False)
    seq = Column('ATTENDANCE_CYCLE_SEQ', Integer, nullable=False)
    sifid = Column('SIF_ID', String(32))                  
    start_date = Column('ATTENDANCE_CYCLE_START_DATE', Date, nullable=False)
    cycle_type = Column('ATTENDANCE_CYCLE_TYPE', String(50), nullable=False)                  
    created_by_portal_OID = Column('CREATED_BY_PORTAL_OID', BigInteger)
    created_by_task_OID = Column('CREATED_BY_TASK_OID', BigInteger)
    created_by_user_OID = Column('CREATED_BY_USER_OID', BigInteger)                  
    created_ip = Column('CREATED_IP', String(100))
    created_on = Column('CREATED_ON', DateTime)                      
    last_updated_by_portal_OID = Column('LAST_UPDATED_BY_PORTAL_OID', BigInteger)
    last_updated_by_task_OID = Column('LAST_UPDATED_BY_TASK_OID', BigInteger)
    last_updated_by_user_OID = Column('LAST_UPDATED_BY_USER_OID', BigInteger)
    last_updated_ip = Column('LAST_UPDATED_IP', String(100))                     
    last_updated_on = Column('LAST_UPDATED', DateTime)

    report_code = '991191'
    csv_header = [
        'SCHOOL_YEAR',
        'SCHOOL_CODE',
        'ATTENDANCE_CYCLE_CODE',
        'ATTENDANCE_CYCLE_DESCRIPTION',
        'ATTENDANCE_CYCLE_END_DATE',
        'GB_DESCRIPTION',
        'READ_ONLY',
        'ATTENDANCE_CYCLE_SEQ',
        'SIF_ID',
        'ATTENDANCE_CYCLE_START_DATE',
        'ATTENDANCE_CYCLE_TYPE',
        'CREATED_BY_PORTAL_OID',
        'CREATED_BY_TASK_OID',
        'CREATED_BY_USER_OID',
        'CREATED_IP',
        'CREATED_ON',
        'LAST_UPDATED_BY_PORTAL_OID',
        'LAST_UPDATED_BY_TASK_OID',
        'LAST_UPDATED_BY_USER_OID',
        'LAST_UPDATED_IP',
        'LAST_UPDATED',
    ]

    @classmethod
    def from_csv(cls, row):
        return cls(
            school_year                = row[0],
            school_code                = row[1],
            code                       = row[2],
            description                = row[3],
            end_date                   = utils.genesis_to_date(row[4]),
            gb_description             = row[5],
            read_only                  = utils.genesis_to_boolean(row[6]),
            seq                        = row[7],
            sifid                      = row[8],
            start_date                 = utils.genesis_to_date(row[9]),
            cycle_type                 = row[10],
            created_by_portal_OID      = row[11],
            created_by_task_OID        = row[12],
            created_by_user_OID        = row[13],
            created_ip                 = row[14],
            created_on                 = utils.genesis_to_datetime(row[15]),
            last_updated_by_portal_OID = row[16],
            last_updated_by_task_OID   = row[17],
            last_updated_by_user_OID   = row[18],
            last_updated_ip            = row[19],
            last_updated_on            = utils.genesis_to_datetime(row[20]),
        )

    def __repr__(self):
        return (
            f"SchoolAttendanceCycle "
            f"school_year={self.school_year} "
            f"school_code={self.school_code} "
            f"code={self.code}"
        )
