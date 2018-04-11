from sqlalchemy import Column, Integer, String, Boolean, BigInteger, Date, DateTime
from sqlalchemy.orm import relationship
from AR.tables import Base
from AR.tables import utils

class Student(Base):
    __tablename__ = 'STUDENTS'

    ability_level = Column('ABILITY_LEVEL', String(8))
    academically_disadvantaged = Column('ACADEMICALLY_DISADVANTAGED', Boolean, nullable=False)
    academic_independent_program = Column('ACADEMIC_INDEPENDENT_PROGRAM', Boolean, nullable=False)
    age = Column('AGE', Integer, nullable=False)
    alternate_lunch_location = Column('ALTERNATE_LUNCH_LOCATION', Boolean, nullable=False)
    alternative_ed_program = Column('ALTERNATIVE_ED_PROGRAM', String(8))
    attending_district_code = Column('ATTENDING_DISTRICT_CODE', String(9))
    avid_student = Column('AVID_STUDENT', Boolean, nullable=False)
    bilingual_program = Column('BILINGUAL_PROGRAM', String(8))
    birth_certificate_document = Column('BIRTH_CERTIFICATE_DOCUMENT', String(255))
    birth_certificate_number = Column('BIRTH_CERTIFICATE_NUMBER', String(40))
    birth_place_city = Column('BIRTH_PLACE_CITY', String(50))
    birth_place_country = Column('BIRTH_PLACE_COUNTRY', String(8))
    birth_place_state = Column('BIRTH_PLACE_STATE', String(2))
    case_manager_code = Column('CASE_MANAGER_CODE', String(10))
    child_of_dist_employee = Column('CHILD_OF_DIST_EMPLOYEE', Boolean, nullable=False)
    citizenship = Column('CITIZENSHIP', String(50))
    citizenship_code = Column('CITIZENSHIP_CODE', String(8))
    class_of = Column('CLASS_OF', Integer, nullable=False)
    compensatory_ed_program = Column('COMPENSATORY_ED_PROGRAM', String(8))
    counselor_id = Column('COUNSELOR_ID', String(10))
    counselor_name = Column('COUNSELOR_NAME', String(110))
    created_by_portal_oid = Column('CREATED_BY_PORTAL_OID', BigInteger)
    created_by_task_oid = Column('CREATED_BY_TASK_OID', BigInteger)
    created_by_user_oid = Column('CREATED_BY_USER_OID', BigInteger)
    created_ip = Column('CREATED_IP', String(100))
    created_on = Column('CREATED_ON', DateTime)
    current_entry_in_district = Column('CURRENT_ENTRY_IN_DISTRICT', Date)
    current_homeroom = Column('CURRENT_HOMEROOM', String(25))
    current_homeroom_teacher = Column('CURRENT_HOMEROOM_TEACHER', String(110))
    current_program_entry_date = Column('CURRENT_PROGRAM_ENTRY_DATE', Date)
    current_program_exit_date = Column('CURRENT_PROGRAM_EXIT_DATE', Date)
    current_program_type_code = Column('CURRENT_PROGRAM_TYPE_CODE', String(8), nullable=False)
    current_school = Column('CURRENT_SCHOOL', String(8), nullable=False)
    current_withdrawal_date = Column('CURRENT_WITHDRAWAL_DATE', Date)
    current_entry_date = Column('CURRENT_ENTRY_DATE', Date)
    curriculum = Column('CURRICULUM', String(8))
    date_of_birth = Column('DATE_OF_BIRTH', Date, nullable=False)
    date_of_graduation = Column('DATE_OF_GRADUATION', Date)
    eighth_tech_lit = Column('EIGHTH_TECH_LIT', String(3))
    enrollment_status = Column('ENROLLMENT_STATUS', String(10))
    exclusion_flag = Column('EXCLUSION_FLAG', String(8))
    family_code = Column('FAMILY_CODE', String(8))
    first_entry_us_school = Column('FIRST_ENTRY_US_SCHOOL', Date)
    first_name = Column('FIRST_NAME', String(30), nullable=False)
    gender = Column('GENDER', String(11))
    gender_code = Column('GENDER_CODE', String(1), nullable=False)
    gifted_talented = Column('GIFTED_TALENTED', Boolean, nullable=False)
    grade_level = Column('GRADE_LEVEL', String(3), nullable=False)
    graduated = Column('GRADUATED', Boolean, nullable=False)
    group_home = Column('GROUP_HOME', Boolean, nullable=False)
    high_school_entry_date = Column('HIGH_SCHOOL_ENTRY_DATE', Date)
    homebound_status = Column('HOMEBOUND_STATUS', String(3), nullable=False)
    home_language = Column('HOME_LANGUAGE', String(255))
    home_language_code = Column('HOME_LANGUAGE_CODE', String(8))
    homeless_code = Column('HOMELESS_CODE', Boolean, nullable=False)
    homeroom = Column('HOMEROOM', String(25))
    homeroom_teacher = Column('HOMEROOM_TEACHER', String(110))
    home_school = Column('HOME_SCHOOL', String(8))
    home_schooled = Column('HOME_SCHOOLED', Boolean, nullable=False)
    home_school_reason = Column('HOME_SCHOOL_REASON', String(8))
    hr_teacher_first_last = Column('HR_TEACHER_FIRST_LAST', String(110))
    immigration_status = Column('IMMIGRATION_STATUS', String(100))
    immigration_status_code = Column('IMMIGRATION_STATUS_CODE', String(8))
    last_name = Column('LAST_NAME', String(50), nullable=False)
    last_updated_by_portal_oid = Column('LAST_UPDATED_BY_PORTAL_OID', BigInteger)
    last_updated_by_task_oid = Column('LAST_UPDATED_BY_TASK_OID', BigInteger)
    last_updated_by_user_oid = Column('LAST_UPDATED_BY_USER_OID', BigInteger)
    last_updated_ip = Column('LAST_UPDATED_IP', String(100))
    last_updated = Column('LAST_UPDATED', DateTime)
    legacy_student_id = Column('LEGACY_STUDENT_ID', String(15))
    lep_immigrant_program = Column('LEP_IMMIGRANT_PROGRAM', String(8))
    locker = Column('LOCKER', String(8))
    lunch_balance = Column('LUNCH_BALANCE', BigInteger)
    lunch_code = Column('LUNCH_CODE', String(8))
    lunch_pin = Column('LUNCH_PIN', String(20))
    middle_name = Column('MIDDLE_NAME', String(30))
    migrant = Column('MIGRANT', Boolean, nullable=False)
    military_affiliation_code = Column('MILITARY_AFFILIATION_CODE', String(8))
    military_indicator = Column('MILITARY_INDICATOR', String(2))
    military_exclusion = Column('MILITARY_EXCLUSION', Boolean, nullable=False)
    municipality_code = Column('MUNICIPALITY_CODE', String(8))
    nickname = Column('NICKNAME', String(30))
    non_public_student = Column('NON_PUBLIC_STUDENT', Boolean, nullable=False)
    notify_before_reg = Column('NOTIFY_BEFORE_REG', Boolean, nullable=False)
    openreg_student_oid = Column('OPENREG_STUDENT_OID', BigInteger)
    original_entry_grade_level = Column('ORIGINAL_ENTRY_GRADE_LEVEL', String(3))
    original_entry_in_district = Column('ORIGINAL_ENTRY_IN_DISTRICT', Date)
    original_entry_in_school = Column('ORIGINAL_ENTRY_IN_SCHOOL', Date)
    original_entry_school_code = Column('ORIGINAL_ENTRY_SCHOOL_CODE', String(8))
    pcc_entry_code = Column('PCC_ENTRY_CODE', String(3), nullable=False)
    pcc_withdrawal_code = Column('PCC_WITHDRAWAL_CODE', String(3))
    penalty_points = Column('PENALTY_POINTS', Integer, nullable=False)
    post_education_plan = Column('POST_EDUCATION_PLAN', String(8))
    previous_county_code = Column('PREVIOUS_COUNTY_CODE', String(2))
    previous_district_code = Column('PREVIOUS_DISTRICT_CODE', String(9))
    previous_grade_level = Column('PREVIOUS_GRADE_LEVEL', String(3))
    previous_school_code = Column('PREVIOUS_SCHOOL_CODE', String(10))
    previous_state_school_code = Column('PREVIOUS_STATE_SCHOOL_CODE', String(10))
    primary_language = Column('PRIMARY_LANGUAGE', String(255))
    primary_language_code = Column('PRIMARY_LANGUAGE_CODE', String(8))
    race_american_indian = Column('RACE_AMERICAN_INDIAN', Boolean, nullable=False)
    race_asian = Column('RACE_ASIAN', Boolean, nullable=False)
    race_black = Column('RACE_BLACK', Boolean, nullable=False)
    race_hispanic = Column('RACE_HISPANIC', Boolean, nullable=False)
    race_pacific = Column('RACE_PACIFIC', Boolean, nullable=False)
    race_white = Column('RACE_WHITE', Boolean, nullable=False)
    registration_date = Column('REGISTRATION_DATE', Date, nullable=False)
    reg_note = Column('REG_NOTE', String)
    resident_district_code = Column('RESIDENT_DISTRICT_CODE', String(9))
    retained = Column('RETAINED', Boolean, nullable=False)
    school_before_summer_school = Column('SCHOOL_BEFORE_SUMMER_SCHOOL', String(20))
    school_to_work = Column('SCHOOL_TO_WORK', Boolean, nullable=False)
    school_year = Column('SCHOOL_YEAR', String(7), nullable=False, primary_key=True)
    session_code = Column('SESSION_CODE', String(8))
    share_free_red_lunch_info = Column('SHARE_FREE_RED_LUNCH_INFO', Boolean)
    shift_code = Column('SHIFT_CODE', String(8))
    show_504_icon = Column('SHOW_504_ICON', Boolean, nullable=False)
    sif_id = Column('SIF_ID', String(32))
    social_security_number = Column('SOCIAL_SECURITY_NUMBER', String(11))
    spec_ed = Column('SPEC_ED', String(3), nullable=False)
    spec_ed_self_contained = Column('SPEC_ED_SELF_CONTAINED', Boolean, nullable=False)
    spec_ed_status = Column('SPEC_ED_STATUS', String(50))
    spec_ed_status_code = Column('SPEC_ED_STATUS_CODE', String(8))
    sports_ineligibility_reason = Column('SPORTS_INELIGIBILITY_REASON', String(30))
    state_id_number = Column('STATE_ID_NUMBER', String(15))
    code_504 = Column('CODE_504', Boolean, nullable=False)
    code_504_docid = Column('CODE_504_DOCID', String(255))
    ell_docid = Column('ELL_DOCID', String(255))
    student_id = Column('STUDENT_ID', String(15), nullable=False, primary_key=True)
    iep_docid = Column('IEP_DOCID', String(255))
    irs_docid = Column('IRS_DOCID', String(255))
    student_name = Column('STUDENT_NAME', String(115), nullable=False)
    suffix = Column('SUFFIX', String(8))
    summer_school_enrollment = Column('SUMMER_SCHOOL_ENROLLMENT', String(20))
    supplemental_instruction = Column('SUPPLEMENTAL_INSTRUCTION', String(8))
    team_code = Column('TEAM_CODE', String(8))
    transportation_code = Column('TRANSPORTATION_CODE', String(8))
    truant = Column('TRUANT', String(8))
    tuition_code = Column('TUITION_CODE', String(8))
    used_in_state_reporting = Column('USED_IN_STATE_REPORTING', Boolean, nullable=False)
    us_entry_date = Column('US_ENTRY_DATE', Date)
    viceprincipal_id = Column('VICEPRINCIPAL_ID', String(10))
    vocational_ed_district = Column('VOCATIONAL_ED_DISTRICT', String(9))
    vocational_ed_program = Column('VOCATIONAL_ED_PROGRAM', String(8))
    vocational_school_code = Column('VOCATIONAL_SCHOOL_CODE', String(10))
    vocational_shared_time = Column('VOCATIONAL_SHARED_TIME', String(15))
    vocational_program_code = Column('VOCATIONAL_PROGRAM_CODE', String(8))
    waive_birthplace_info = Column('WAIVE_BIRTHPLACE_INFO', Boolean, nullable=False)
    year_of_graduation = Column('YEAR_OF_GRADUATION', Integer, nullable=False)

    student_schedule = relationship("StudentSchedule", back_populates='student')

    report_code = '991016'
    csv_header = [
        'ABILITY_LEVEL',
        'ACADEMICALLY_DISADVANTAGED',
        'ACADEMIC_INDEPENDENT_PROGRAM',
        'AGE',
        'ALTERNATE_LUNCH_LOCATION',
        'ALTERNATIVE_ED_PROGRAM',
        'ATTENDING_DISTRICT_CODE',
        'AVID_STUDENT',
        'BILINGUAL_PROGRAM',
        'BIRTH_CERTIFICATE_DOCUMENT',
        'BIRTH_CERTIFICATE_NUMBER',
        'BIRTH_PLACE_CITY',
        'BIRTH_PLACE_COUNTRY',
        'BIRTH_PLACE_STATE',
        'CASE_MANAGER_CODE',
        'CHILD_OF_DIST_EMPLOYEE',
        'CITIZENSHIP',
        'CITIZENSHIP_CODE',
        'CLASS_OF',
        'COMPENSATORY_ED_PROGRAM',
        'COUNSELOR_ID',
        'COUNSELOR_NAME',
        'CREATED_BY_PORTAL_OID',
        'CREATED_BY_TASK_OID',
        'CREATED_BY_USER_OID',
        'CREATED_IP',
        'CREATED_ON',
        'CURRENT_ENTRY_IN_DISTRICT',
        'CURRENT_HOMEROOM',
        'CURRENT_HOMEROOM_TEACHER',
        'CURRENT_PROGRAM_ENTRY_DATE',
        'CURRENT_PROGRAM_EXIT_DATE',
        'CURRENT_PROGRAM_TYPE_CODE',
        'CURRENT_SCHOOL',
        'CURRENT_WITHDRAWAL_DATE',
        'CURRENT_ENTRY_DATE',
        'CURRICULUM',
        'DATE_OF_BIRTH',
        'DATE_OF_GRADUATION',
        'EIGHTH_TECH_LIT',
        'ENROLLMENT_STATUS',
        'EXCLUSION_FLAG',
        'FAMILY_CODE',
        'FIRST_ENTRY_US_SCHOOL',
        'FIRST_NAME',
        'GENDER',
        'GENDER_CODE',
        'GIFTED_TALENTED',
        'GRADE_LEVEL',
        'GRADUATED',
        'GROUP_HOME',
        'HIGH_SCHOOL_ENTRY_DATE',
        'HOMEBOUND_STATUS',
        'HOME_LANGUAGE',
        'HOME_LANGUAGE_CODE',
        'HOMELESS_CODE',
        'HOMEROOM',
        'HOMEROOM_TEACHER',
        'HOME_SCHOOL',
        'HOME_SCHOOLED',
        'HOME_SCHOOL_REASON',
        'HR_TEACHER_FIRST_LAST',
        'IMMIGRATION_STATUS',
        'IMMIGRATION_STATUS_CODE',
        'LAST_NAME',
        'LAST_UPDATED_BY_PORTAL_OID',
        'LAST_UPDATED_BY_TASK_OID',
        'LAST_UPDATED_BY_USER_OID',
        'LAST_UPDATED_IP',
        'LAST_UPDATED',
        'LEGACY_STUDENT_ID',
        'LEP_IMMIGRANT_PROGRAM',
        'LOCKER',
        'LUNCH_BALANCE',
        'LUNCH_CODE',
        'LUNCH_PIN',
        'MIDDLE_NAME',
        'MIGRANT',
        'MILITARY_AFFILIATION_CODE',
        'MILITARY_INDICATOR',
        'MILITARY_EXCLUSION',
        'MUNICIPALITY_CODE',
        'NICKNAME',
        'NON_PUBLIC_STUDENT',
        'NOTIFY_BEFORE_REG',
        'OPENREG_STUDENT_OID',
        'ORIGINAL_ENTRY_GRADE_LEVEL',
        'ORIGINAL_ENTRY_IN_DISTRICT',
        'ORIGINAL_ENTRY_IN_SCHOOL',
        'ORIGINAL_ENTRY_SCHOOL_CODE',
        'PCC_ENTRY_CODE',
        'PCC_WITHDRAWAL_CODE',
        'PENALTY_POINTS',
        'POST_EDUCATION_PLAN',
        'PREVIOUS_COUNTY_CODE',
        'PREVIOUS_DISTRICT_CODE',
        'PREVIOUS_GRADE_LEVEL',
        'PREVIOUS_SCHOOL_CODE',
        'PREVIOUS_STATE_SCHOOL_CODE',
        'PRIMARY_LANGUAGE',
        'PRIMARY_LANGUAGE_CODE',
        'RACE_AMERICAN_INDIAN',
        'RACE_ASIAN',
        'RACE_BLACK',
        'RACE_HISPANIC',
        'RACE_PACIFIC',
        'RACE_WHITE',
        'REGISTRATION_DATE',
        'REG_NOTE',
        'RESIDENT_DISTRICT_CODE',
        'RETAINED',
        'SCHOOL_BEFORE_SUMMER_SCHOOL',
        'SCHOOL_TO_WORK',
        'SCHOOL_YEAR',
        'SESSION_CODE',
        'SHARE_FREE_RED_LUNCH_INFO',
        'SHIFT_CODE',
        'SHOW_504_ICON',
        'SIF_ID',
        'SOCIAL_SECURITY_NUMBER',
        'SPEC_ED',
        'SPEC_ED_SELF_CONTAINED',
        'SPEC_ED_STATUS',
        'SPEC_ED_STATUS_CODE',
        'SPORTS_INELIGIBILITY_REASON',
        'STATE_ID_NUMBER',
        'CODE_504',
        'CODE_504_DOCID',
        'ELL_DOCID',
        'STUDENT_ID',
        'IEP_DOCID',
        'IRS_DOCID',
        'STUDENT_NAME',
        'SUFFIX',
        'SUMMER_SCHOOL_ENROLLMENT',
        'SUPPLEMENTAL_INSTRUCTION',
        'TEAM_CODE',
        'TRANSPORTATION_CODE',
        'TRUANT',
        'TUITION_CODE',
        'USED_IN_STATE_REPORTING',
        'US_ENTRY_DATE',
        'VICEPRINCIPAL_ID',
        'VOCATIONAL_ED_DISTRICT',
        'VOCATIONAL_ED_PROGRAM',
        'VOCATIONAL_SCHOOL_CODE',
        'VOCATIONAL_SHARED_TIME',
        'VOCATIONAL_PROGRAM_CODE',
        'WAIVE_BIRTHPLACE_INFO',
        'YEAR_OF_GRADUATION'
    ]

    @classmethod
    def from_csv(cls, row):
        return cls(
            ability_level = row[0],
            academically_disadvantaged      = utils.genesis_to_boolean(row[1]),
            academic_independent_program    = utils.genesis_to_boolean(row[2]),
            age                             = row[3],
            alternate_lunch_location        = utils.genesis_to_boolean(row[4]),
            alternative_ed_program          = row[5],
            attending_district_code         = row[6],
            avid_student                    = utils.genesis_to_boolean(row[7]),
            bilingual_program               = row[8],
            birth_certificate_document      = row[9],
            birth_certificate_number        = row[10],
            birth_place_city                = row[11],
            birth_place_country             = row[12],
            birth_place_state               = row[13],
            case_manager_code               = row[14],
            child_of_dist_employee          = utils.genesis_to_boolean(row[15]),
            citizenship                     = row[16],
            citizenship_code                = row[17],
            class_of                        = row[18],
            compensatory_ed_program         = row[19],
            counselor_id                    = row[20],
            counselor_name                  = row[21],
            created_by_portal_oid           = row[22],
            created_by_task_oid             = row[23],
            created_by_user_oid             = row[24],
            created_ip                      = row[25],
            created_on                      = utils.genesis_to_datetime(row[26]),
            current_entry_in_district       = utils.genesis_to_date(row[27]),
            current_homeroom                = row[28],
            current_homeroom_teacher        = row[29],
            current_program_entry_date      = utils.genesis_to_date(row[30]),
            current_program_exit_date       = utils.genesis_to_date(row[31]),
            current_program_type_code       = row[32],
            current_school                  = row[33],
            current_withdrawal_date         = utils.genesis_to_date(row[34]),
            current_entry_date              = utils.genesis_to_date(row[35]),
            curriculum                      = row[36],
            date_of_birth                   = utils.genesis_to_date(row[37]),
            date_of_graduation              = utils.genesis_to_date(row[38]),
            eighth_tech_lit                 = row[39],
            enrollment_status               = row[40],
            exclusion_flag                  = row[41],
            family_code                     = row[42],
            first_entry_us_school           = utils.genesis_to_date(row[43]),
            first_name                      = row[44],
            gender                          = row[45],
            gender_code                     = row[46],
            gifted_talented                 = utils.genesis_to_boolean(row[47]),
            grade_level                     = row[48],
            graduated                       = utils.genesis_to_boolean(row[49]),
            group_home                      = utils.genesis_to_boolean(row[50]),
            high_school_entry_date          = utils.genesis_to_date(row[51]),
            homebound_status                = row[52],
            home_language                   = row[53],
            home_language_code              = row[54],
            homeless_code                   = utils.genesis_to_boolean(row[55]),
            homeroom                        = row[56],
            homeroom_teacher                = row[57],
            home_school                     = row[58],
            home_schooled                   = utils.genesis_to_boolean(row[59]),
            home_school_reason              = row[60],
            hr_teacher_first_last           = row[61],
            immigration_status              = row[62],
            immigration_status_code         = row[63],
            last_name                       = row[64],
            last_updated_by_portal_oid      = row[65],
            last_updated_by_task_oid        = row[66],
            last_updated_by_user_oid        = row[67],
            last_updated_ip                 = row[68],
            last_updated                    = utils.genesis_to_datetime(row[69]),
            legacy_student_id               = row[70],
            lep_immigrant_program           = row[71],
            locker                          = row[72],
            lunch_balance                   = row[73],
            lunch_code                      = row[74],
            lunch_pin                       = row[75],
            middle_name                     = row[76],
            migrant                         = utils.genesis_to_boolean(row[77]),
            military_affiliation_code       = row[78],
            military_indicator              = row[79],
            military_exclusion              = utils.genesis_to_boolean(row[80]),
            municipality_code               = row[81],
            nickname                        = row[82],
            non_public_student              = utils.genesis_to_boolean(row[83]),
            notify_before_reg               = utils.genesis_to_boolean(row[84]),
            openreg_student_oid             = row[85],
            original_entry_grade_level      = row[86],
            original_entry_in_district      = utils.genesis_to_date(row[87]),
            original_entry_in_school        = utils.genesis_to_date(row[88]),
            original_entry_school_code      = row[89],
            pcc_entry_code                  = row[90],
            pcc_withdrawal_code             = row[91],
            penalty_points                  = row[92],
            post_education_plan             = row[93],
            previous_county_code            = row[94],
            previous_district_code          = row[95],
            previous_grade_level            = row[96],
            previous_school_code            = row[97],
            previous_state_school_code      = row[98],
            primary_language                = row[99],
            primary_language_code           = row[100],
            race_american_indian            = utils.genesis_to_boolean(row[101]),
            race_asian                      = utils.genesis_to_boolean(row[102]),
            race_black                      = utils.genesis_to_boolean(row[103]),
            race_hispanic                   = utils.genesis_to_boolean(row[104]),
            race_pacific                    = utils.genesis_to_boolean(row[105]),
            race_white                      = utils.genesis_to_boolean(row[106]),
            registration_date               = utils.genesis_to_date(row[107]),
            reg_note                        = row[108],
            resident_district_code          = row[109],
            retained                        = utils.genesis_to_boolean(row[110]),
            school_before_summer_school     = row[111],
            school_to_work                  = utils.genesis_to_boolean(row[112]),
            school_year                     = row[113],
            session_code                    = row[114],
            share_free_red_lunch_info       = utils.genesis_to_boolean(row[115]),
            shift_code                      = row[116],
            show_504_icon                   = utils.genesis_to_boolean(row[117]),
            sif_id                          = row[118],
            social_security_number          = row[119],
            spec_ed                         = row[120],
            spec_ed_self_contained          = utils.genesis_to_boolean(row[121]),
            spec_ed_status                  = row[122],
            spec_ed_status_code             = row[123],
            sports_ineligibility_reason     = row[124],
            state_id_number                 = row[125],
            code_504                        = utils.genesis_to_boolean(row[126]),
            code_504_docid                  = row[127],
            ell_docid                       = row[128],
            student_id                      = row[129],
            iep_docid                       = row[130],
            irs_docid                       = row[131],
            student_name                    = row[132],
            suffix                          = row[133],
            summer_school_enrollment        = row[134],
            supplemental_instruction        = row[135],
            team_code                       = row[136],
            transportation_code             = row[137],
            truant                          = row[138],
            tuition_code                    = row[139],
            used_in_state_reporting         = utils.genesis_to_boolean(row[140]),
            us_entry_date                   = utils.genesis_to_date(row[141]),
            viceprincipal_id                = row[142],
            vocational_ed_district          = row[143],
            vocational_ed_program           = row[144],
            vocational_school_code          = row[145],
            vocational_shared_time          = row[146],
            vocational_program_code         = row[147],
            waive_birthplace_info           = utils.genesis_to_boolean(row[148]),
            year_of_graduation              = row[149]
        )

    def __repr__(self):
        return "<Student(student_id={}, first_name={}, last_name={})>".format(self.student_id, self.first_name, self.last_name) 
