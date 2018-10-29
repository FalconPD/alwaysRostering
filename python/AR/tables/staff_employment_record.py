from sqlalchemy import Column, String, BigInteger, Date, DateTime, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from AR.tables import Base, utils 

class StaffEmploymentRecord(Base):
    __tablename__ = 'STAFF_EMPLOYMENT_RECORDS'
#    __table_args__ = (
#        ForeignKeyConstraint(['TEACHER_ID'], ['DISTRICT_TEACHERS.TEACHER_ID']),
#    )

    created_by_portal_oid = Column('CREATED_BY_PORTAL_OID',  BigInteger)
    created_by_task_oid = Column('CREATED_BY_TASK_OID',  BigInteger)
    created_by_user_oid = Column('CREATED_BY_USER_OID',  BigInteger)
    created_ip = Column('CREATED_IP', String(100))
    created_on = Column('CREATED_ON',  DateTime)
    end_date = Column('END_DATE', Date)
    entry_code = Column('ENTRY_CODE', String(2))
    exit_code = Column('EXIT_CODE', String(2))
    last_updated_by_portal_oid = Column('LAST_UPDATED_BY_PORTAL_OID',  BigInteger)
    last_updated_by_task_oid = Column('LAST_UPDATED_BY_TASK_OID',  BigInteger)
    last_updated_by_user_oid = Column('LAST_UPDATED_BY_USER_OID',  BigInteger)
    last_updated_ip = Column('LAST_UPDATED_IP', String(100))
    last_updated = Column('LAST_UPDATED',  DateTime)
    object_id = Column('OBJECT_ID', BigInteger, nullable=False, primary_key=True)
    start_date = Column('START_DATE', Date, nullable=False)
    teacher_id = Column('TEACHER_ID', String(10), nullable=False)

    #district_teacher = relationship('DistrictTeacher', back_populates='employment_records')

    report_code = '991114',
    csv_header = [ 
        'CREATED_BY_PORTAL_OID',
        'CREATED_BY_TASK_OID',
        'CREATED_BY_USER_OID',
        'CREATED_IP',
        'CREATED_ON',
        'END_DATE',
        'ENTRY_CODE',
        'EXIT_CODE',
        'LAST_UPDATED_BY_PORTAL_OID',
        'LAST_UPDATED_BY_TASK_OID',
        'LAST_UPDATED_BY_USER_OID',
        'LAST_UPDATED_IP',
        'LAST_UPDATED',
        'OBJECT_ID',
        'START_DATE',
        'TEACHER_ID',
    ]

    @classmethod
    def from_csv(cls, row):
        return cls(
            created_by_portal_oid       = row[0],
            created_by_task_oid         = row[1], 
            created_by_user_oid         = row[2],
            created_ip                  = row[3],
            created_on                  = utils.genesis_to_datetime(row[4]),
            end_date                    = utils.genesis_to_date(row[5]),
            entry_code                  = row[6],
            exit_code                   = row[7],
            last_updated_by_portal_oid  = row[8],
            last_updated_by_task_oid    = row[9],
            last_updated_by_user_oid    = row[10],
            last_updated_ip             = row[11],
            last_updated                = utils.genesis_to_datetime(row[12]),
            object_id                   = row[13],
            start_date                  = utils.genesis_to_date(row[14]),
            teacher_id                  = row[15],
        )

    def __repr__(self):
        return (
                "StaffEmploymentRecord "
                "teacher_id={} "
                "start_date={} "
                "entry_code={} "
                "end_date={} "
                "exit_code={}"
            ).format(
                self.teacher_id,
                self.start_date,
                self.entry_code,
                self.end_date,
                self.exit_code,
            )
