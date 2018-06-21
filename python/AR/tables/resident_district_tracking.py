from sqlalchemy import Column, String, Date, BigInteger, DateTime
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy.orm import relationship
from AR.tables import Base
from AR.tables import utils

class ResidentDistrictTracking(Base):
    __tablename__ = 'RESIDENT_DISTRICT_TRACKING'
    __table_args__ = (
        ForeignKeyConstraint(
            [
                'STUDENT_ID',
                'SCHOOL_YEAR',
            ],
            [
                'STUDENTS.STUDENT_ID',
                'STUDENTS.SCHOOL_YEAR',
            ],
        ),
    )

    created_by_portal_oid = Column('CREATED_BY_PORTAL_OID', BigInteger)
    created_by_task_oid = Column('CREATED_BY_TASK_OID', BigInteger)
    created_by_user_oid = Column('CREATED_BY_USER_OID', BigInteger)
    created_ip = Column('CREATED_IP', String(100))
    created_on = Column('CREATED_ON', DateTime)
    endDate = Column('END_DATE', Date)
    last_updated_by_portal_oid = Column('LAST_UPDATED_BY_PORTAL_OID',
        BigInteger)
    last_updated_by_task_oid = Column('LAST_UPDATED_BY_TASK_OID', BigInteger)
    last_updated_by_user_oid = Column('LAST_UPDATED_BY_USER_OID', BigInteger)
    last_updated_ip = Column('LAST_UPDATED_IP', String(100))
    last_updated = Column('LAST_UPDATED', DateTime)
    objectid = Column('OBJECT_ID', BigInteger, nullable=False, primary_key=True)
    resident_county_code = Column('RESIDENT_COUNTY_CODE', String(2))
    resident_district_code = Column('RESIDENT_DISTRICT_CODE', String(50))
    resident_school_code = Column('RESIDENT_SCHOOL_CODE', String(50))
    school_year = Column('SCHOOL_YEAR', String(7), nullable=False)
    start_date = Column('START_DATE', Date, nullable=False)
    student_id = Column('STUDENT_ID', String(15))

    report_code = '991007'
    csv_header = [ 
        'CREATED_BY_PORTAL_OID',
        'CREATED_BY_TASK_OID',
        'CREATED_BY_USER_OID',
        'CREATED_IP',
        'CREATED_ON',
        'END_DATE',
        'LAST_UPDATED_BY_PORTAL_OID',
        'LAST_UPDATED_BY_TASK_OID',
        'LAST_UPDATED_BY_USER_OID',
        'LAST_UPDATED_IP',
        'LAST_UPDATED',
        'OBJECT_ID',
        'RESIDENT_COUNTY_CODE',
        'RESIDENT_DISTRICT_CODE',
        'RESIDENT_SCHOOL_CODE',
        'SCHOOL_YEAR',
        'START_DATE',
        'STUDENT_ID',
    ]

    @classmethod
    def from_csv(cls, row):
        return cls(
            created_by_portal_oid       = row[0],
            created_by_task_oid         = row[1],
            created_by_user_oid         = row[2],
            created_ip                  = row[3],
            created_on                  = utils.genesis_to_datetime(row[4]),
            endDate                     = utils.genesis_to_date(row[5]),
            last_updated_by_portal_oid  = row[6],
            last_updated_by_task_oid    = row[7],
            last_updated_by_user_oid    = row[8],
            last_updated_ip             = row[9],
            last_updated                = utils.genesis_to_datetime(row[10]),
            objectid                    = row[11],
            resident_county_code        = row[12],
            resident_district_code      = row[13],
            resident_school_code        = row[14],
            school_year                 = row[15],
            start_date                  = utils.genesis_to_date(row[16]),
            student_id                  = row[17],
        )

    def __repr__(self):
        return (
                "ResidentDistrictTracking "
                "student_id={} "
                "school_year={} "
                "resident_county_code={} "
                "resident_district_code={} "
                "resident_school_code={}"
            ).format(
                self.student_id,
                self.school_year,
                self.resident_county_code,
                self.resident_district_code,
                self.resident_school_code
            )
