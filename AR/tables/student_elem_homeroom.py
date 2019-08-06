from sqlalchemy import Column, String, BigInteger, DateTime
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy.orm import relationship
from AR.tables import Base
from AR.tables import utils

class StudentElementaryHomeroom(Base):
    __tablename__ = 'STUDENT_ELEM_HOMEROOM'
    __table_args__ = (
        ForeignKeyConstraint(
            [
                'STUDENT_ID',
                'SCHOOL_CODE',
                'GRADE_LEVEL'
            ],
            [
                'STUDENTS.STUDENT_ID',
                'STUDENTS.CURRENT_SCHOOL',
                'STUDENTS.GRADE_LEVEL'
            ]
        ),
    )

    created_by_portal_oid = Column('CREATED_BY_PORTAL_OID', BigInteger)
    created_by_task_oid = Column('CREATED_BY_TASK_OID', BigInteger)
    created_by_user_oid = Column('CREATED_BY_USER_OID', BigInteger)
    created_ip = Column('CREATED_IP', String(100))
    created_on = Column('CREATED_ON', DateTime)
    grade_level = Column('GRADE_LEVEL', String(10), nullable=False,
        primary_key=True)
    homeroom = Column('HOMEROOM', String(25))
    last_updated_by_portal_oid = Column('LAST_UPDATED_BY_PORTAL_OID', BigInteger)
    last_updated_by_task_oid = Column('LAST_UPDATED_BY_TASK_OID', BigInteger)
    last_updated_by_user_oid = Column('LAST_UPDATED_BY_USER_OID', BigInteger)
    last_updated_ip = Column('LAST_UPDATED_IP', String(100))
    last_updated = Column('LAST_UPDATED', DateTime)
    school_code = Column('SCHOOL_CODE', String(8), nullable=False,
        primary_key=True)
    student_id = Column('STUDENT_ID', String(15), nullable=False,
        primary_key=True)
    teacher_id = Column('TEACHER_ID', String(10))

    student = relationship('Student', back_populates='elementary_homeroom')

    report_code = '991076'
    csv_header = [
        'CREATED_BY_PORTAL_OID',
        'CREATED_BY_TASK_OID',
        'CREATED_BY_USER_OID',
        'CREATED_IP',
        'CREATED_ON',
        'GRADE_LEVEL',
        'HOMEROOM',
        'LAST_UPDATED_BY_PORTAL_OID',
        'LAST_UPDATED_BY_TASK_OID',
        'LAST_UPDATED_BY_USER_OID',
        'LAST_UPDATED_IP',
        'LAST_UPDATED',
        'SCHOOL_CODE',
        'STUDENT_ID',
        'TEACHER_ID'
    ]

    @classmethod
    def from_csv(cls, row):
        return cls(
            created_by_portal_oid       = row[0],
            created_by_task_oid         = row[1],
            created_by_user_oid         = row[2],
            created_ip                  = row[3],
            created_on                  = utils.genesis_to_datetime(row[4]),
            grade_level                 = row[5],
            homeroom                    = row[6],
            last_updated_by_portal_oid  = row[7],
            last_updated_by_task_oid    = row[8],
            last_updated_by_user_oid    = row[9],
            last_updated_ip             = row[10],
            last_updated                = utils.genesis_to_datetime(row[11]),
            school_code                 = row[12],
            student_id                  = row[13],
            teacher_id                  = row[14],
        )

    def __repr__(self):
        return (
            (
                "StudentElementaryHomeroom "
                "student_id={} "
                "homeroom={} "
                "teacher_id={} "
            ).format(
                self.student_id,
                self.homeroom,
                self.teacher_id
            )
        )
