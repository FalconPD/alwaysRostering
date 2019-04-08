from sqlalchemy import Column, BigInteger, Boolean, Date, DateTime, String
from sqlalchemy import Integer
from AR.tables import utils, Base

class LunchCode(Base):
    __tablename__ = 'LUNCH_CODES'

    categorical = Column('CATEGORICAL', Boolean, nullable=False)
    code = Column('CODE', String, nullable=False, primary_key=True)
    created_by_portal_oid = Column('CREATED_BY_PORTAL_OID', BigInteger)
    created_by_task_oid = Column('CREATED_BY_TASK_OID', BigInteger)
    created_by_user_oid = Column('CREATED_BY_USER_OID', BigInteger)
    created_ip = Column('CREATED_IP', String)
    created_on = Column('CREATED_ON', DateTime)
    dc_foster = Column('IS_DC_FOSTER', Boolean, nullable=False)
    dc_SNAP = Column('IS_DC_SNAP', Boolean, nullable=False)
    dc_TANF = Column('IS_DC_TANF', Boolean, nullable=False)
    denied = Column('IS_DENIED', Boolean, nullable=False)
    description = Column('DESCRIPTION', String, nullable=False)
    direct_certification = Column('IS_DC', Boolean, nullable=False)
    foster_letter = Column('FOSTER_LETTER', Boolean, nullable=False)
    free = Column('IS_FREE', Boolean, nullable=False)
    free_foster = Column('IS_FREE_FOST', Boolean, nullable=False)
    free_income = Column('IS_FREE_INCOME', Boolean, nullable=False)
    free_tanf = Column('IS_FREE_TANF', Boolean, nullable=False)
    head_start_or_local_official = Column('HEAD_START', Boolean, nullable=False)
    hide_on_application = Column('HIDE_ON_APPLICATION', Boolean, nullable=False)
    ignore = Column('IS_IGNORE', Boolean, nullable=False)
    incomplete = Column('INCOMPLETE', Boolean, nullable=False)
    last_updated_by_portal_oid = Column('LAST_UPDATED_BY_PORTAL_OID', BigInteger)
    last_updated_by_task_oid = Column('LAST_UPDATED_BY_TASK_OID', BigInteger)
    last_updated_by_user_oid = Column('LAST_UPDATED_BY_USER_OID', BigInteger)
    last_updated_ip = Column('LAST_UPDATED_IP', String)
    last_updated = Column('LAST_UPDATED', DateTime)
    reduced = Column('IS_REDUCED', Boolean, nullable=False)
    school_year = Column('SCHOOL_YEAR', String, nullable=False, primary_key=True)
    seq = Column('SEQ', Integer, nullable=False)

    report_code = '991183'
    csv_header = [
        'CATEGORICAL',
        'CODE',
        'CREATED_BY_PORTAL_OID',
        'CREATED_BY_TASK_OID',
        'CREATED_BY_USER_OID',
        'CREATED_IP',
        'CREATED_ON',
        'IS_DC_FOSTER',
        'IS_DC_SNAP',
        'IS_DC_TANF',
        'IS_DENIED',
        'DESCRIPTION',
        'IS_DC',
        'FOSTER_LETTER',
        'IS_FREE',
        'IS_FREE_FOST',
        'IS_FREE_INCOME',
        'IS_FREE_TANF',
        'HEAD_START',
        'HIDE_ON_APPLICATION',
        'IS_IGNORE',
        'INCOMPLETE',
        'LAST_UPDATED_BY_PORTAL_OID',
        'LAST_UPDATED_BY_TASK_OID',
        'LAST_UPDATED_BY_USER_OID',
        'LAST_UPDATED_IP',
        'LAST_UPDATED',
        'IS_REDUCED',
        'SCHOOL_YEAR',
        'SEQ',
    ]

    @classmethod
    def from_csv(cls, row):
        return cls(
            categorical = utils.genesis_to_boolean(row[0]),
            code = row[1],
            created_by_portal_oid = row[2],
            created_by_task_oid = row[3],
            created_by_user_oid = row[4],
            created_ip = row[5],
            created_on = utils.genesis_to_datetime(row[6]),
            dc_foster = utils.genesis_to_boolean(row[7]),
            dc_SNAP = utils.genesis_to_boolean(row[8]),
            dc_TANF = utils.genesis_to_boolean(row[9]),
            denied = utils.genesis_to_boolean(row[10]),
            description = row[11],
            direct_certification = utils.genesis_to_boolean(row[12]),
            foster_letter = utils.genesis_to_boolean(row[13]),
            free = utils.genesis_to_boolean(row[14]),
            free_foster = utils.genesis_to_boolean(row[15]),
            free_income = utils.genesis_to_boolean(row[16]),
            free_tanf = utils.genesis_to_boolean(row[17]),
            head_start_or_local_official = utils.genesis_to_boolean(row[18]),
            hide_on_application = utils.genesis_to_boolean(row[19]),
            ignore = utils.genesis_to_boolean(row[20]),
            incomplete = utils.genesis_to_boolean(row[21]),
            last_updated_by_portal_oid = row[22],
            last_updated_by_task_oid = row[23],
            last_updated_by_user_oid = row[24],
            last_updated_ip = row[25],
            last_updated = utils.genesis_to_datetime(row[26]),
            reduced = utils.genesis_to_boolean(row[27]),
            school_year = row[28],
            seq = row[29],
        )

    def __repr__(self):
        return (
            f"LunchCode code={self.code} "
            f"free={self.free} reduced={self.reduced}"
        )
