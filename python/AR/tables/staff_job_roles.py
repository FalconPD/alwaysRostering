from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Boolean, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from AR.tables import Base
from AR.tables import utils

class StaffJobRole(Base):
    __tablename__ = 'STAFF_JOB_ROLES'
    __table_args__ = (
        ForeignKeyConstraint(['TEACHER_ID', 'SCHOOL_YEAR'],
            ['DISTRICT_TEACHERS.TEACHER_ID', 'DISTRICT_TEACHERS.SCHOOL_YEAR']),
    )

    age_group_taught = Column('AGE_GROUP_TAUGHT', String(1))
    county_code_assigned = Column('COUNTY_CODE_ASSIGNED', String(2))
    created_by_portal_oid = Column('CREATED_BY_PORTAL_OID', BigInteger)
    created_by_task_oid = Column('CREATED_BY_TASK_OID', BigInteger)
    created_by_user_oid = Column('CREATED_BY_USER_OID', BigInteger)
    created_ip = Column('CREATED_IP', String(100))
    created_on = Column('CREATED_ON', DateTime)
    credential_type = Column('CREDENTIAL_TYPE',	String(1))
    district_code_assigned = Column('DISTRICT_CODE_ASSIGNED', String(50))
    dont_send_to_njsmart = Column('DONT_SEND_TO_NJSMART', Boolean, nullable=False)
    full_time_equivalency = Column('FULL_TIME_EQUIVALENCY', BigInteger)
    hqt_qualification_status = Column('HQT_QUALIFICATION_STATUS', String(1))
    job_code = Column('JOB_CODE', String(4))
    job_code_subcategory = Column('JOB_CODE_SUBCATEGORY', String(1))
    last_updated_by_portal_oid = Column('LAST_UPDATED_BY_PORTAL_OID', BigInteger)
    last_updated_by_task_oid = Column('LAST_UPDATED_BY_TASK_OID', BigInteger)
    last_updated_by_user_oid = Column('LAST_UPDATED_BY_USER_OID', BigInteger)
    last_updated_ip = Column('LAST_UPDATED_IP',	String(100))
    last_updated = Column('LAST_UPDATED', DateTime)
    number_of_classes_taught = Column('NUMBER_OF_CLASSES_TAUGHT', Integer)
    reason_for_not_being_hq = Column('REASON_FOR_NOT_BEING_HQ',	String(3))
    role_seq = Column('ROLE_SEQ', Integer, nullable=False, primary_key=True)
    school_code_assigned = Column('SCHOOL_CODE_ASSIGNED', String(50))
    school_year = Column('SCHOOL_YEAR', String(7), nullable=False, primary_key=True)
    support_to_being_hq = Column('SUPPORT_TO_BEING_HQ', String(3))
    teacher_id = Column('TEACHER_ID', String(10), nullable=False, primary_key=True)
    teacher_prep = Column('TEACHER_PREP', String(1))

    district_teacher = relationship('DistrictTeacher', back_populates='job_roles')

    report_code = '990993'
    csv_header = [
        'AGE_GROUP_TAUGHT',
        'COUNTY_CODE_ASSIGNED',
        'CREATED_BY_PORTAL_OID',
        'CREATED_BY_TASK_OID',
        'CREATED_BY_USER_OID',
        'CREATED_IP',
        'CREATED_ON',
        'CREDENTIAL_TYPE',
        'DISTRICT_CODE_ASSIGNED',
        'DONT_SEND_TO_NJSMART',
        'FULL_TIME_EQUIVALENCY',
        'HQT_QUALIFICATION_STATUS',
        'JOB_CODE',
        'JOB_CODE_SUBCATEGORY',
        'LAST_UPDATED_BY_PORTAL_OID',
        'LAST_UPDATED_BY_TASK_OID',
        'LAST_UPDATED_BY_USER_OID',
        'LAST_UPDATED_IP',
        'LAST_UPDATED',
        'NUMBER_OF_CLASSES_TAUGHT',
        'REASON_FOR_NOT_BEING_HQ',
        'ROLE_SEQ',
        'SCHOOL_CODE_ASSIGNED',
        'SCHOOL_YEAR',
        'SUPPORT_TO_BEING_HQ',
        'TEACHER_ID',
        'TEACHER_PREP'
    ]

    @classmethod
    def from_csv(cls, row):
        return cls( 
            age_group_taught            = row[0],
            county_code_assigned        = row[1],
            created_by_portal_oid       = row[2],
            created_by_task_oid         = row[3],
            created_by_user_oid         = row[4],
            created_ip                  = row[5],
            created_on                  = utils.genesis_to_datetime(row[6]),
            credential_type             = row[7],
            district_code_assigned      = row[8],
            dont_send_to_njsmart        = utils.genesis_to_boolean(row[9]),
            full_time_equivalency       = row[10],
            hqt_qualification_status    = row[11],
            job_code                    = row[12],
            job_code_subcategory        = row[13],
            last_updated_by_portal_oid  = row[14],
            last_updated_by_task_oid    = row[15],
            last_updated_by_user_oid    = row[16],
            last_updated_ip             = row[17],
            last_updated                = utils.genesis_to_datetime(row[18]),
            number_of_classes_taught    = row[19],
            reason_for_not_being_hq     = row[20],
            role_seq                    = row[21],
            school_code_assigned        = row[22],
            school_year                 = row[23],
            support_to_being_hq         = row[24],
            teacher_id                  = row[25],
            teacher_prep                = row[26]
        )

    def __repr__(self):
        return '{} {} {}'.format(self.role_seq, self.job_code,
            self.school_code_assigned) 
