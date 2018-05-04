from sqlalchemy import Column, Integer, String, Boolean, BigInteger, Date, DateTime, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from AR.tables import Base
from AR.tables import utils
import re
import logging

class DistrictTeacher(Base):
    __tablename__ = 'DISTRICT_TEACHERS'
    teacher_address1 = Column('TEACHER_ADDRESS1', String(50))
    teacher_address2 = Column('TEACHER_ADDRESS2', String(50))
    is_admin = Column('IS_ADMIN', Boolean, nullable=False)
    alt_route_program = Column('ALT_ROUTE_PROGRAM', String(3))
    teacher_area_code = Column('TEACHER_AREA_CODE', Integer)
    is_athletic_trainer = Column('IS_ATHLETIC_TRAINER', Boolean, nullable=False)
    case_manager = Column('CASE_MANAGER', Boolean, nullable=False)
    teacher_cell_phone = Column('TEACHER_CELL_PHONE', String(15))
    certification_status = Column('CERTIFICATION_STATUS', Boolean, nullable=False)
    teacher_city = Column('TEACHER_CITY', String(30))
    coordinator_504 = Column('COORDINATOR_504', Boolean, nullable=False)
    counselor_id = Column('COUNSELOR_ID', String(10))
    counselor_name = Column('COUNSELOR_NAME', String(110))
    country_code = Column('COUNTRY_CODE', String(8))
    county_code = Column('COUNTY_CODE', String(8))
    created_by_portal_oid = Column('CREATED_BY_PORTAL_OID',  BigInteger)
    created_by_task_oid = Column('CREATED_BY_TASK_OID',  BigInteger)
    created_by_user_oid = Column('CREATED_BY_USER_OID',  BigInteger)
    created_ip = Column('CREATED_IP', String(100))
    created_on = Column('CREATED_ON',  DateTime)
    data_1 = Column('DATA_1', String(255))
    date_of_birth = Column('DATE_OF_BIRTH',  Date)
    is_disciplinarian = Column('IS_DISCIPLINARIAN', Boolean, nullable=False)
    do_not_export_schoolfi = Column('DO_NOT_EXPORT_SCHOOLFI', Boolean, nullable=False)
    do_not_import_lastname = Column('DO_NOT_IMPORT_LASTNAME', Boolean, nullable=False)
    teacher_email = Column('TEACHER_EMAIL', String(255))
    employment_status = Column('EMPLOYMENT_STATUS', String(1), nullable=False)
    ethnicity = Column('ETHNICITY', Boolean,)
    evaluation_of_staff = Column('EVALUATION_OF_STAFF', String(2))
    exceptional_salary = Column('EXCEPTIONAL_SALARY', String(1))
    exclude_from_auto_dialer = Column('EXCLUDE_FROM_AUTO_DIALER', Boolean, nullable=False)
    teacher_first_name = Column('TEACHER_FIRST_NAME', String(40))
    former_name = Column('FORMER_NAME', String(50))
    gender_code = Column('GENDER_CODE', String(1))
    highest_ed_completed = Column('HIGHEST_ED_COMPLETED', String(2))
    home_phone_listed = Column('HOME_PHONE_LISTED', Boolean, nullable=False)
    teacher_homework_url = Column('TEACHER_HOMEWORK_URL', String(255))
    include_in_njsmart = Column('INCLUDE_IN_NJSMART', Boolean, nullable=False)
    spoken_language = Column('SPOKEN_LANGUAGE', String(3))
    teacher_last_name = Column('TEACHER_LAST_NAME', String(50))
    last_updated_by_portal_oid = Column('LAST_UPDATED_BY_PORTAL_OID',  BigInteger)
    last_updated_by_task_oid = Column('LAST_UPDATED_BY_TASK_OID',  BigInteger)
    last_updated_by_user_oid = Column('LAST_UPDATED_BY_USER_OID',  BigInteger)
    last_updated_ip = Column('LAST_UPDATED_IP', String(100))
    last_updated = Column('LAST_UPDATED',  DateTime)
    lep_instructor_cred_type = Column('LEP_INSTRUCTOR_CRED_TYPE', String(1))
    is_library = Column('IS_LIBRARY', Boolean, nullable=False)
    is_long_term_substitute = Column('IS_LONG_TERM_SUBSTITUTE', Boolean, nullable=False)
    mep_session_type = Column('MEP_SESSION_TYPE', String(1))
    teacher_middle_name = Column('TEACHER_MIDDLE_NAME', String(30))
    migrant_ed_prg_staff_cat = Column('MIGRANT_ED_PRG_STAFF_CAT', String(1))
    teacher_name = Column('TEACHER_NAME', String(110))
    national_board_award = Column('NATIONAL_BOARD_AWARD',  Date)
    njsmart_sub_teacher_id = Column('NJSMART_SUB_TEACHER_ID', String(10))
    notes = Column('NOTES', String(4000))
    is_nurse = Column('IS_NURSE', Boolean, nullable=False)
    other_id_number = Column('OTHER_ID_NUMBER', String(50))
    other_staff_member = Column('OTHER_STAFF_MEMBER', Boolean, nullable=False)
    prefix_code = Column('PREFIX_CODE', String(8))
    is_principal = Column('IS_PRINCIPAL', Boolean, nullable=False)
    race_american_indian = Column('RACE_AMERICAN_INDIAN', Boolean, nullable=False)
    race_asian = Column('RACE_ASIAN', Boolean, nullable=False)
    race_black = Column('RACE_BLACK', Boolean, nullable=False)
    race_pacific = Column('RACE_PACIFIC', Boolean, nullable=False)
    race_white = Column('RACE_WHITE', Boolean, nullable=False)
    related_service_provider = Column('RELATED_SERVICE_PROVIDER', Boolean, nullable=False)
    resource_teacher = Column('RESOURCE_TEACHER', Boolean, nullable=False)
    salary = Column('SALARY', Integer)
    school_year = Column('SCHOOL_YEAR', String(7), nullable=False, primary_key=True)
    sep_prg_contr_service_cat = Column('SEP_PRG_CONTR_SERVICE_CAT', String(2))
    shared_teacher = Column('SHARED_TEACHER', Boolean, nullable=False)
    shared_teacher_id_1 = Column('SHARED_TEACHER_ID_1', String(10))
    shared_teacher_id_2 = Column('SHARED_TEACHER_ID_2', String(10))
    shared_teacher_id_3 = Column('SHARED_TEACHER_ID_3', String(10))
    shared_teacher_id_4 = Column('SHARED_TEACHER_ID_4', String(10))
    shared_teacher_id_5 = Column('SHARED_TEACHER_ID_5', String(10))
    shared_teacher_id_6 = Column('SHARED_TEACHER_ID_6', String(10))
    sif_id = Column('SIF_ID', String(32))
    signature = Column('SIGNATURE', String(110))
    signature_title = Column('SIGNATURE_TITLE', String(110))
    spec_ed_team = Column('SPEC_ED_TEAM', String(100))
    teacher_soc_sec_number = Column('TEACHER_SOC_SEC_NUMBER', String(11))
    state_code = Column('STATE_CODE', String(2))
    state_id_number = Column('STATE_ID_NUMBER', String(15))
    suffix_code = Column('SUFFIX_CODE', String(8))
    teacher = Column('TEACHER', Boolean, nullable=False)
    teacher_code = Column('TEACHER_CODE', String(12))
    teacher_id = Column('TEACHER_ID', String(10), primary_key=True)
    teacher_url = Column('TEACHER_URL', String(255))
    teacher_telephone_exchange = Column('TEACHER_TELEPHONE_EXCHANGE', Integer)
    teacher_telephone_number = Column('TEACHER_TELEPHONE_NUMBER', Integer)
    title_i_prg_staff_cat = Column('TITLE_I_PRG_STAFF_CAT', String(1))
    prep_program = Column('PREP_PROGRAM', String(3))
    is_viceprincipal = Column('IS_VICEPRINCIPAL', Boolean, nullable=False)
    teacher_voice_mail = Column('TEACHER_VOICE_MAIL', String(255))
    years_in_lea = Column('YEARS_IN_LEA', Integer)
    years_in_nj = Column('YEARS_IN_NJ', Integer)
    years_of_prior_exp = Column('YEARS_OF_PRIOR_EXP', Integer)
    teacher_zipcode = Column('TEACHER_ZIPCODE', String(15))

    job_roles = relationship('StaffJobRole', back_populates='district_teacher')

    report_code = '991018',
    csv_header = [ 
        'TEACHER_ADDRESS1',
        'TEACHER_ADDRESS2',
        'IS_ADMIN',
        'ALT_ROUTE_PROGRAM',
        'TEACHER_AREA_CODE',
        'IS_ATHLETIC_TRAINER',
        'CASE_MANAGER',
        'TEACHER_CELL_PHONE',
        'CERTIFICATION_STATUS',
        'TEACHER_CITY',
        'COORDINATOR_504',
        'COUNSELOR_ID',
        'COUNSELOR_NAME',
        'COUNTRY_CODE',
        'COUNTY_CODE',
        'CREATED_BY_PORTAL_OID',
        'CREATED_BY_TASK_OID',
        'CREATED_BY_USER_OID',
        'CREATED_IP',
        'CREATED_ON',
        'DATA_1',
        'DATE_OF_BIRTH',
        'IS_DISCIPLINARIAN',
        'DO_NOT_EXPORT_SCHOOLFI',
        'DO_NOT_IMPORT_LASTNAME',
        'TEACHER_EMAIL',
        'EMPLOYMENT_STATUS',
        'ETHNICITY',
        'EVALUATION_OF_STAFF',
        'EXCEPTIONAL_SALARY',
        'EXCLUDE_FROM_AUTO_DIALER',
        'TEACHER_FIRST_NAME',
        'FORMER_NAME',
        'GENDER_CODE',
        'HIGHEST_ED_COMPLETED',
        'HOME_PHONE_LISTED',
        'TEACHER_HOMEWORK_URL',
        'INCLUDE_IN_NJSMART',
        'SPOKEN_LANGUAGE',
        'TEACHER_LAST_NAME',
        'LAST_UPDATED_BY_PORTAL_OID',
        'LAST_UPDATED_BY_TASK_OID',
        'LAST_UPDATED_BY_USER_OID',
        'LAST_UPDATED_IP',
        'LAST_UPDATED',
        'LEP_INSTRUCTOR_CRED_TYPE',
        'IS_LIBRARY',
        'IS_LONG_TERM_SUBSTITUTE',
        'MEP_SESSION_TYPE',
        'TEACHER_MIDDLE_NAME',
        'MIGRANT_ED_PRG_STAFF_CAT',
        'TEACHER_NAME',
        'NATIONAL_BOARD_AWARD',
        'NJSMART_SUB_TEACHER_ID',
        'NOTES',
        'IS_NURSE',
        'OTHER_ID_NUMBER',
        'OTHER_STAFF_MEMBER',
        'PREFIX_CODE',
        'IS_PRINCIPAL',
        'RACE_AMERICAN_INDIAN',
        'RACE_ASIAN',
        'RACE_BLACK',
        'RACE_PACIFIC',
        'RACE_WHITE',
        'RELATED_SERVICE_PROVIDER',
        'RESOURCE_TEACHER',
        'SALARY',
        'SCHOOL_YEAR',
        'SEP_PRG_CONTR_SERVICE_CAT',
        'SHARED_TEACHER',
        'SHARED_TEACHER_ID_1',
        'SHARED_TEACHER_ID_2',
        'SHARED_TEACHER_ID_3',
        'SHARED_TEACHER_ID_4',
        'SHARED_TEACHER_ID_5',
        'SHARED_TEACHER_ID_6',
        'SIF_ID',
        'SIGNATURE',
        'SIGNATURE_TITLE',
        'SPEC_ED_TEAM',
        'TEACHER_SOC_SEC_NUMBER',
        'STATE_CODE',
        'STATE_ID_NUMBER',
        'SUFFIX_CODE',
        'TEACHER',
        'TEACHER_CODE',
        'TEACHER_ID',
        'TEACHER_URL',
        'TEACHER_TELEPHONE_EXCHANGE',
        'TEACHER_TELEPHONE_NUMBER',
        'TITLE_I_PRG_STAFF_CAT',
        'PREP_PROGRAM',
        'IS_VICEPRINCIPAL',
        'TEACHER_VOICE_MAIL',
        'YEARS_IN_LEA',
        'YEARS_IN_NJ',
        'YEARS_OF_PRIOR_EXP',
        'TEACHER_ZIPCODE'
    ]

    @classmethod
    def from_csv(cls, row):
        return cls(
            teacher_address1            = row[0],
            teacher_address2            = row[1],
            is_admin                    = utils.genesis_to_boolean(row[2]),
            alt_route_program           = row[3],
            teacher_area_code           = row[4],
            is_athletic_trainer         = utils.genesis_to_boolean(row[5]),
            case_manager                = utils.genesis_to_boolean(row[6]),
            teacher_cell_phone          = row[7],
            certification_status        = utils.genesis_to_boolean(row[8]),
            teacher_city                = row[9],
            coordinator_504             = utils.genesis_to_boolean(row[10]),
            counselor_id                = row[11],
            counselor_name              = row[12],
            country_code                = row[13],
            county_code                 = row[14],
            created_by_portal_oid       = row[15],
            created_by_task_oid         = row[16],
            created_by_user_oid         = row[17],
            created_ip                  = row[18],
            created_on                  = utils.genesis_to_datetime(row[19]),
            data_1                      = row[20],
            date_of_birth               = utils.genesis_to_date(row[21]),
            is_disciplinarian           = utils.genesis_to_boolean(row[22]),
            do_not_export_schoolfi      = utils.genesis_to_boolean(row[23]),
            do_not_import_lastname      = utils.genesis_to_boolean(row[24]),
            teacher_email               = row[25],
            employment_status           = row[26],
            ethnicity                   = utils.genesis_to_boolean(row[27]),
            evaluation_of_staff         = row[28],
            exceptional_salary          = row[29],
            exclude_from_auto_dialer    = utils.genesis_to_boolean(row[30]),
            teacher_first_name          = row[31],
            former_name                 = row[32],
            gender_code                 = row[33],
            highest_ed_completed        = row[34],
            home_phone_listed           = utils.genesis_to_boolean(row[35]),
            teacher_homework_url        = row[36],
            include_in_njsmart          = utils.genesis_to_boolean(row[37]),
            spoken_language             = row[38],
            teacher_last_name           = row[39],
            last_updated_by_portal_oid  = row[40],
            last_updated_by_task_oid    = row[41],
            last_updated_by_user_oid    = row[42],
            last_updated_ip             = row[43],
            last_updated                = utils.genesis_to_datetime(row[44]),
            lep_instructor_cred_type    = row[45],
            is_library                  = utils.genesis_to_boolean(row[46]),
            is_long_term_substitute     = utils.genesis_to_boolean(row[47]),
            mep_session_type            = row[48],
            teacher_middle_name         = row[49],
            migrant_ed_prg_staff_cat    = row[50],
            teacher_name                = row[51],
            national_board_award        = utils.genesis_to_date(row[52]),
            njsmart_sub_teacher_id      = row[53],
            notes                       = row[54],
            is_nurse                    = utils.genesis_to_boolean(row[55]),
            other_id_number             = row[56],
            other_staff_member          = utils.genesis_to_boolean(row[57]),
            prefix_code                 = row[58],
            is_principal                = utils.genesis_to_boolean(row[59]),
            race_american_indian        = utils.genesis_to_boolean(row[60]),
            race_asian                  = utils.genesis_to_boolean(row[61]),
            race_black                  = utils.genesis_to_boolean(row[62]),
            race_pacific                = utils.genesis_to_boolean(row[63]),
            race_white                  = utils.genesis_to_boolean(row[64]),
            related_service_provider    = utils.genesis_to_boolean(row[65]),
            resource_teacher            = utils.genesis_to_boolean(row[66]),
            salary                      = row[67],
            school_year                 = row[68],
            sep_prg_contr_service_cat   = row[69],
            shared_teacher              = utils.genesis_to_boolean(row[70]),
            shared_teacher_id_1         = row[71],
            shared_teacher_id_2         = row[72],
            shared_teacher_id_3         = row[73],
            shared_teacher_id_4         = row[74],
            shared_teacher_id_5         = row[75],
            shared_teacher_id_6         = row[76],
            sif_id                      = row[77],
            signature                   = row[78],
            signature_title             = row[79],
            spec_ed_team                = row[80],
            teacher_soc_sec_number      = row[81],
            state_code                  = row[82],
            state_id_number             = row[83],
            suffix_code                 = row[84],
            teacher                     = utils.genesis_to_boolean(row[85]),
            teacher_code                = row[86],
            teacher_id                  = row[87],
            teacher_url                 = row[88],
            teacher_telephone_exchange  = row[89],
            teacher_telephone_number    = row[90],
            title_i_prg_staff_cat       = row[91],
            prep_program                = row[92],
            is_viceprincipal            = utils.genesis_to_boolean(row[93]),
            teacher_voice_mail          = row[94],
            years_in_lea                = row[95],
            years_in_nj                 = row[96],
            years_of_prior_exp          = row[97],
            teacher_zipcode             = row[98]
        )

    def __repr__(self):
        return '{} {} {}'.format(self.teacher_id, self.teacher_first_name, self.teacher_last_name)

    # Staff first names may be improperly capitalized
    @property
    def first_name(self):
        if self.teacher_first_name.isupper():
            logging.warning('{} has all uppercase first name'.format(self))
            return self.teacher_first_name.title()
        return self.teacher_first_name

    # Staff last names may be improperly capitalized and half day
    # kindergarten teachers may have AM/PM after their last name
    @property
    def last_name(self):
        name_last = re.sub(r' (AM|PM)$', '', self.teacher_last_name, count=1)
        if name_last.isupper():
            logging.warning('{} has all uppercase last name'.format(self))
            return name_last.title()
        return name_last

    # The preferred staff email is data_1 (user_id) @monroe.k12.nj.us
    # The user_id is guaranteed unique. Also, it should be lowercase
    @property
    def email(self):
        if self.data_1 == '':
            logging.warning('{} does not have a user_id (data_1)'.format(self))
            return None
        return self.data_1.lower() + '@monroe.k12.nj.us'
