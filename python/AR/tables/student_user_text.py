from sqlalchemy import Column, String, BigInteger, DateTime, orm, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from AR.tables import Base
from AR.tables import utils

class StudentUserText(Base):
    __tablename__ = 'STUDENT_USER_TEXT'
    __table_args__ = (
        ForeignKeyConstraint(['STUDENT_ID', 'SCHOOL_YEAR'],
            ['STUDENTS.STUDENT_ID', 'STUDENTS.SCHOOL_YEAR']),
    )

    code = Column('CODE', String(8), nullable=False, primary_key=True)
    created_by_portal_oid = Column('CREATED_BY_PORTAL_OID', BigInteger)
    created_by_task_oid = Column('CREATED_BY_TASK_OID', BigInteger)
    created_by_user_oid = Column('CREATED_BY_USER_OID', BigInteger)
    created_ip = Column('CREATED_IP', String(100))
    created_on = Column('CREATED_ON', DateTime)
    last_updated_by_portal_oid = Column('LAST_UPDATED_BY_PORTAL_OID', BigInteger)
    last_updated_by_task_oid = Column('LAST_UPDATED_BY_TASK_OID', BigInteger)
    last_updated_by_user_oid = Column('LAST_UPDATED_BY_USER_OID', BigInteger)
    last_updated_ip = Column('LAST_UPDATED_IP', String(100))
    last_updated = Column('LAST_UPDATED', DateTime)
    school_year = Column('SCHOOL_YEAR', String(7), nullable=False, primary_key=True)
    student_id = Column('STUDENT_ID', String(15), nullable=False, primary_key=True)
    value = Column('VALUE', String(255))

    student = relationship('Student', back_populates='student_user_text')

    report_code = '991017'
    csv_header = [
        'CODE',
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
        'SCHOOL_YEAR',
        'STUDENT_ID',
        'VALUE'
    ]

    @classmethod
    def from_csv(cls, row):
        return cls(
            code = row[0],
            created_by_portal_oid       = row[1],
            created_by_task_oid         = row[2],
            created_by_user_oid         = row[3],
            created_ip                  = row[4],
            created_on                  = utils.genesis_to_datetime(row[5]),
            last_updated_by_portal_oid  = row[6],
            last_updated_by_task_oid    = row[7],
            last_updated_by_user_oid    = row[8],
            last_updated_ip             = row[9],
            last_updated                = utils.genesis_to_datetime(row[10]),
            school_year                 = row[11],
            student_id                  = row[12],
            value                       = row[13]
        )

    def __repr__(self):
        return "{}: {}".format(self.code, self.value) 
