from sqlalchemy import Column, Integer, String, Boolean, BigInteger, Float, DateTime, Date, orm
from AR.tables import Base
from AR.tables import utils

class School(Base):
    __tablename__ = 'SCHOOLS'
    daily_to_post_class = Column('DAILY_TO_POST_CLASS', Boolean, nullable=False)
    hr_to_post_daily = Column('HR_TO_POST_DAILY', Boolean, nullable=False)
    allow_hr_prop_emails = Column('ALLOW_HR_PROP_EMAILS', Boolean, nullable=False)
    allow_hr_update = Column('ALLOW_HR_UPDATE', Boolean, nullable=False)
    period_to_overwrite_section = Column('PERIOD_TO_OVERWRITE_SECTION', Boolean, nullable=False)
    prior_date_hr_to_post_daily = Column('PRIOR_DATE_HR_TO_POST_DAILY', Boolean, nullable=False)
    allow_gb_update_all_grades = Column('ALLOW_GB_UPDATE_ALL_GRADES', Boolean, nullable=False)
    allow_gb_update_fg = Column('ALLOW_GB_UPDATE_FG', Boolean, nullable=False)
    alternate_code = Column('ALTERNATE_CODE', String(20))
    is_alternate_program = Column('IS_ALTERNATE_PROGRAM', Boolean, nullable=False)
    building_code = Column('BUILDING_CODE', String(8), nullable=False)
    ceeb_code = Column('CEEB_CODE', String(8))
    is_charter_school = Column('IS_CHARTER_SCHOOL', Boolean, nullable=False)
    is_choice = Column('IS_CHOICE', Boolean, nullable=False)
    collect_ood_nj_smart_students = Column('COLLECT_OOD_NJ_SMART_STUDENTS', Boolean, nullable=False)
    school_count_students = Column('SCHOOL_COUNT_STUDENTS', Boolean, nullable=False)
    created_by_portal_oid = Column('CREATED_BY_PORTAL_OID', BigInteger)
    created_by_task_oid = Column('CREATED_BY_TASK_OID', BigInteger)
    created_by_user_oid = Column('CREATED_BY_USER_OID', BigInteger)
    created_ip = Column('CREATED_IP', String(100))
    created_on = Column('CREATED_ON', DateTime)
    default_schedule_view = Column('DEFAULT_SCHEDULE_VIEW', String(25))
    is_esy_school = Column('IS_ESY_SCHOOL', Boolean, nullable=False)
    exclude_prek_njsmart_state = Column('EXCLUDE_PREK_NJSMART_STATE', Boolean, nullable=False)
    exclude_reged_prek_njsmart = Column('EXCLUDE_REGED_PREK_NJSMART', Boolean, nullable=False)
    excluded_school_from_njassa = Column('EXCLUDED_SCHOOL_FROM_NJASSA', Boolean, nullable=False)
    excluded_school_from_njsmart = Column('EXCLUDED_SCHOOL_FROM_NJSMART', Boolean, nullable=False)
    excluded_from_state_sped = Column('EXCLUDED_FROM_STATE_SPED', Boolean, nullable=False)
    fall_eligibility_credits = Column('FALL_ELIGIBILITY_CREDITS', Float, nullable=False)
    fall_eligibility_cred2014 = Column('FALL_ELIGIBILITY_CRED2014', Float, nullable=False)
    federal_school_code = Column('FEDERAL_SCHOOL_CODE', String(50))
    for_parents_module = Column('FOR_PARENTS_MODULE', Boolean, nullable=False)
    gen_pins_on_registration = Column('GEN_PINS_ON_REGISTRATION', Boolean, nullable=False)
    schedule_print_hide_bus = Column('SCHEDULE_PRINT_HIDE_BUS', Boolean, nullable=False)
    highlight_dup_requests = Column('HIGHLIGHT_DUP_REQUESTS', Boolean, nullable=False)
    honor_rolls = Column('HONOR_ROLLS', String(255))
    hr_assignment_type = Column('HR_ASSIGNMENT_TYPE', String(15))
    hr_period = Column('HR_PERIOD', String(5))
    hr_period2 = Column('HR_PERIOD2', String(5))
    hr_period3 = Column('HR_PERIOD3', String(5))
    is_inact = Column('IS_INACT', Boolean, nullable=False)
    in_district = Column('IN_DISTRICT', Boolean, nullable=False)
    word_day_in_bell = Column('WORD_DAY_IN_BELL', Boolean, nullable=False)
    keep_x_ny_sched_runs = Column('KEEP_X_NY_SCHED_RUNS', Integer)
    last_updated_by_portal_oid = Column('LAST_UPDATED_BY_PORTAL_OID', BigInteger)
    last_updated_by_task_oid = Column('LAST_UPDATED_BY_TASK_OID', BigInteger)
    last_updated_by_user_oid = Column('LAST_UPDATED_BY_USER_OID', BigInteger)
    last_updated_ip = Column('LAST_UPDATED_IP', String(100))
    last_updated = Column('LAST_UPDATED', DateTime)
    locker_combination_cycle = Column('LOCKER_COMBINATION_CYCLE', Integer, nullable=False)
    lock_hr_class_from_daily_prop = Column('LOCK_HR_CLASS_FROM_DAILY_PROP', Boolean, nullable=False)
    non_public_school = Column('NON_PUBLIC_SCHOOL', Boolean, nullable=False)
    override_password = Column('OVERRIDE_PASSWORD', String(20))
    pre_eval_school = Column('PRE_EVAL_SCHOOL', Boolean, nullable=False)
    is_prereg = Column('IS_PREREG', Boolean, nullable=False)
    prereg_school_code = Column('PREREG_SCHOOL_CODE', String(8))
    school_primary_color = Column('SCHOOL_PRIMARY_COLOR', String(10))
    is_private_school_disabled = Column('IS_PRIVATE_SCHOOL_DISABLED', Boolean, nullable=False)
    regional_hs = Column('REGIONAL_HS', Boolean, nullable=False)
    rollover_ny_couns = Column('ROLLOVER_NY_COUNS', Boolean, nullable=False)
    rollover_ny_hr = Column('ROLLOVER_NY_HR', Boolean, nullable=False)
    rollover_home_school = Column('ROLLOVER_HOME_SCHOOL', Boolean, nullable=False)
    rollover_res_school = Column('ROLLOVER_RES_SCHOOL', Boolean, nullable=False)
    rollover_set_grad_date = Column('ROLLOVER_SET_GRAD_DATE', Boolean, nullable=False)
    schedule_cycle_days = Column('SCHEDULE_CYCLE_DAYS', Integer, nullable=False)
    schedule_cycle_days2 = Column('SCHEDULE_CYCLE_DAYS2', Integer, nullable=False)
    schedule_cycle_naming = Column('SCHEDULE_CYCLE_NAMING', String(50))
    schedule_cycle_naming2 = Column('SCHEDULE_CYCLE_NAMING2', String(50))
    school_address1 = Column('SCHOOL_ADDRESS1', String(50))
    school_address2 = Column('SCHOOL_ADDRESS2', String(50))
    school_city = Column('SCHOOL_CITY', String(30))
    state_code = Column('STATE_CODE', String(2))
    school_zipcode = Column('SCHOOL_ZIPCODE', String(11))
    school_category = Column('SCHOOL_CATEGORY', String(10), nullable=False)
    school_code = Column('SCHOOL_CODE', String(8), nullable=False, primary_key=True)
    school_contact_name = Column('SCHOOL_CONTACT_NAME', String(50), nullable=False)
    school_description = Column('SCHOOL_DESCRIPTION', String(100))
    school_email = Column('SCHOOL_EMAIL', String(255))
    school_end_date = Column('SCHOOL_END_DATE', Date)
    school_is_copy_of = Column('SCHOOL_IS_COPY_OF', String(8))
    school_name = Column('SCHOOL_NAME', String(100), nullable=False)
    school_number = Column('SCHOOL_NUMBER', String(8))
    school_office_ext = Column('SCHOOL_OFFICE_EXT', String(10))
    school_office_fax = Column('SCHOOL_OFFICE_FAX', String(15))
    school_office_phone = Column('SCHOOL_OFFICE_PHONE', String(15))
    school_principal = Column('SCHOOL_PRINCIPAL', String(50), nullable=False)
    school_principal_email = Column('SCHOOL_PRINCIPAL_EMAIL', String(255))
    school_principal_ext = Column('SCHOOL_PRINCIPAL_EXT', String(10))
    school_principal_fax = Column('SCHOOL_PRINCIPAL_FAX', String(15))
    school_principal_phone = Column('SCHOOL_PRINCIPAL_PHONE', String(15))
    school_special_designation = Column('SCHOOL_SPECIAL_DESIGNATION', String(15))
    school_start_date = Column('SCHOOL_START_DATE', Date)
    school_sys_admin = Column('SCHOOL_SYS_ADMIN', String(50))
    school_sys_admin_email = Column('SCHOOL_SYS_ADMIN_EMAIL', String(255))
    school_sys_admin_ext = Column('SCHOOL_SYS_ADMIN_EXT', String(10))
    school_sys_admin_fax = Column('SCHOOL_SYS_ADMIN_FAX', String(15))
    school_sys_admin_phone = Column('SCHOOL_SYS_ADMIN_PHONE', String(15))
    school_type_code = Column('SCHOOL_TYPE_CODE', String(8), nullable=False)
    school_url = Column('SCHOOL_URL', String(255))
    school_year = Column('SCHOOL_YEAR', String(7), nullable=False, primary_key=True)
    school_secondary_color = Column('SCHOOL_SECONDARY_COLOR', String(10))
    school_seq = Column('SCHOOL_SEQ', Integer, nullable=False)
    all_schools_on_bell = Column('ALL_SCHOOLS_ON_BELL', Boolean, nullable=False)
    show_gb_district_proj_fg = Column('SHOW_GB_DISTRICT_PROJ_FG', Boolean, nullable=False)
    show_gb_projected_fg = Column('SHOW_GB_PROJECTED_FG', Boolean, nullable=False)
    sif_id = Column('SIF_ID', String(32))
    speced_readonly = Column('SPECED_READONLY', Boolean, nullable=False)
    spring_eligibility_credits = Column('SPRING_ELIGIBILITY_CREDITS', Float, nullable=False)
    spring_eligibility_cred2014 = Column('SPRING_ELIGIBILITY_CRED2014', Float, nullable=False)
    state_county_code = Column('STATE_COUNTY_CODE', String(2))
    state_district_code = Column('STATE_DISTRICT_CODE', String(4))
    state_school_code = Column('STATE_SCHOOL_CODE', String(9))
    student_id_counter = Column('STUDENT_ID_COUNTER', Integer, nullable=False)
    student_pass_distribution = Column('STUDENT_PASS_DISTRIBUTION', String(20))
    att_checkin_pass_location = Column('ATT_CHECKIN_PASS_LOCATION', String(20))
    att_checkin_pass = Column('ATT_CHECKIN_PASS', Boolean, nullable=False)
    student_pass_sort = Column('STUDENT_PASS_SORT', String(50), nullable=False)
    att_checkin_pass_reason = Column('ATT_CHECKIN_PASS_REASON', String(20))
    student_sched_by_sem = Column('STUDENT_SCHED_BY_SEM', Boolean, nullable=False)
    is_summer_school = Column('IS_SUMMER_SCHOOL', Boolean, nullable=False)
    title_1_school = Column('TITLE_1_SCHOOL', Boolean, nullable=False)
    transcript_school_code = Column('TRANSCRIPT_SCHOOL_CODE', String(8))
    random_bell_times = Column('RANDOM_BELL_TIMES', Boolean, nullable=False)
    update_hr_from_sched_screen = Column('UPDATE_HR_FROM_SCHED_SCREEN', Boolean, nullable=False)
    use_gb_grade_for_auto_calc = Column('USE_GB_GRADE_FOR_AUTO_CALC', Boolean, nullable=False)
    use_homeschool_assa = Column('USE_HOMESCHOOL_ASSA', Boolean, nullable=False)
    att_checkin_use_minipass = Column('ATT_CHECKIN_USE_MINIPASS', Boolean, nullable=False)
    use_subsection_descriptions = Column('USE_SUBSECTION_DESCRIPTIONS', Boolean, nullable=False)
    is_vocational = Column('IS_VOCATIONAL', Boolean, nullable=False)

    report_code = '991024'
    csv_header = [
        'DAILY_TO_POST_CLASS',
        'HR_TO_POST_DAILY',
        'ALLOW_HR_PROP_EMAILS',
        'ALLOW_HR_UPDATE',
        'PERIOD_TO_OVERWRITE_SECTION',
        'PRIOR_DATE_HR_TO_POST_DAILY',
        'ALLOW_GB_UPDATE_ALL_GRADES',
        'ALLOW_GB_UPDATE_FG',
        'ALTERNATE_CODE',
        'IS_ALTERNATE_PROGRAM',
        'BUILDING_CODE',
        'CEEB_CODE',
        'IS_CHARTER_SCHOOL',
        'IS_CHOICE',
        'COLLECT_OOD_NJ_SMART_STUDENTS',
        'SCHOOL_COUNT_STUDENTS',
        'CREATED_BY_PORTAL_OID',
        'CREATED_BY_TASK_OID',
        'CREATED_BY_USER_OID',
        'CREATED_IP',
        'CREATED_ON',
        'DEFAULT_SCHEDULE_VIEW',
        'IS_ESY_SCHOOL',
        'EXCLUDE_PREK_NJSMART_STATE',
        'EXCLUDE_REGED_PREK_NJSMART',
        'EXCLUDED_SCHOOL_FROM_NJASSA',
        'EXCLUDED_SCHOOL_FROM_NJSMART',
        'EXCLUDED_FROM_STATE_SPED',
        'FALL_ELIGIBILITY_CREDITS',
        'FALL_ELIGIBILITY_CRED2014',
        'FEDERAL_SCHOOL_CODE',
        'FOR_PARENTS_MODULE',
        'GEN_PINS_ON_REGISTRATION',
        'SCHEDULE_PRINT_HIDE_BUS',
        'HIGHLIGHT_DUP_REQUESTS',
        'HONOR_ROLLS',
        'HR_ASSIGNMENT_TYPE',
        'HR_PERIOD',
        'HR_PERIOD2',
        'HR_PERIOD3',
        'IS_INACT',
        'IN_DISTRICT',
        'WORD_DAY_IN_BELL',
        'KEEP_X_NY_SCHED_RUNS',
        'LAST_UPDATED_BY_PORTAL_OID',
        'LAST_UPDATED_BY_TASK_OID',
        'LAST_UPDATED_BY_USER_OID',
        'LAST_UPDATED_IP',
        'LAST_UPDATED',
        'LOCKER_COMBINATION_CYCLE',
        'LOCK_HR_CLASS_FROM_DAILY_PROP',
        'NON_PUBLIC_SCHOOL',
        'OVERRIDE_PASSWORD',
        'PRE_EVAL_SCHOOL',
        'IS_PREREG',
        'PREREG_SCHOOL_CODE',
        'SCHOOL_PRIMARY_COLOR',
        'IS_PRIVATE_SCHOOL_DISABLED',
        'REGIONAL_HS',
        'ROLLOVER_NY_COUNS',
        'ROLLOVER_NY_HR',
        'ROLLOVER_HOME_SCHOOL',
        'ROLLOVER_RES_SCHOOL',
        'ROLLOVER_SET_GRAD_DATE',
        'SCHEDULE_CYCLE_DAYS',
        'SCHEDULE_CYCLE_DAYS2',
        'SCHEDULE_CYCLE_NAMING',
        'SCHEDULE_CYCLE_NAMING2',
        'SCHOOL_ADDRESS1',
        'SCHOOL_ADDRESS2',
        'SCHOOL_CITY',
        'STATE_CODE',
        'SCHOOL_ZIPCODE',
        'SCHOOL_CATEGORY',
        'SCHOOL_CODE',
        'SCHOOL_CONTACT_NAME',
        'SCHOOL_DESCRIPTION',
        'SCHOOL_EMAIL',
        'SCHOOL_END_DATE',
        'SCHOOL_IS_COPY_OF',
        'SCHOOL_NAME',
        'SCHOOL_NUMBER',
        'SCHOOL_OFFICE_EXT',
        'SCHOOL_OFFICE_FAX',
        'SCHOOL_OFFICE_PHONE',
        'SCHOOL_PRINCIPAL',
        'SCHOOL_PRINCIPAL_EMAIL',
        'SCHOOL_PRINCIPAL_EXT',
        'SCHOOL_PRINCIPAL_FAX',
        'SCHOOL_PRINCIPAL_PHONE',
        'SCHOOL_SPECIAL_DESIGNATION',
        'SCHOOL_START_DATE',
        'SCHOOL_SYS_ADMIN',
        'SCHOOL_SYS_ADMIN_EMAIL',
        'SCHOOL_SYS_ADMIN_EXT',
        'SCHOOL_SYS_ADMIN_FAX',
        'SCHOOL_SYS_ADMIN_PHONE',
        'SCHOOL_TYPE_CODE',
        'SCHOOL_URL',
        'SCHOOL_YEAR',
        'SCHOOL_SECONDARY_COLOR',
        'SCHOOL_SEQ',
        'ALL_SCHOOLS_ON_BELL',
        'SHOW_GB_DISTRICT_PROJ_FG',
        'SHOW_GB_PROJECTED_FG',
        'SIF_ID',
        'SPECED_READONLY',
        'SPRING_ELIGIBILITY_CREDITS',
        'SPRING_ELIGIBILITY_CRED2014',
        'STATE_COUNTY_CODE',
        'STATE_DISTRICT_CODE',
        'STATE_SCHOOL_CODE',
        'STUDENT_ID_COUNTER',
        'STUDENT_PASS_DISTRIBUTION',
        'ATT_CHECKIN_PASS_LOCATION',
        'ATT_CHECKIN_PASS',
        'STUDENT_PASS_SORT',
        'ATT_CHECKIN_PASS_REASON',
        'STUDENT_SCHED_BY_SEM',
        'IS_SUMMER_SCHOOL',
        'TITLE_1_SCHOOL',
        'TRANSCRIPT_SCHOOL_CODE',
        'RANDOM_BELL_TIMES',
        'UPDATE_HR_FROM_SCHED_SCREEN',
        'USE_GB_GRADE_FOR_AUTO_CALC',
        'USE_HOMESCHOOL_ASSA',
        'ATT_CHECKIN_USE_MINIPASS',
        'USE_SUBSECTION_DESCRIPTIONS',
        'IS_VOCATIONAL'
    ]

    @classmethod
    def from_csv(cls, row):
        return cls(
            daily_to_post_class             = utils.genesis_to_boolean(row[0]),
            hr_to_post_daily                = utils.genesis_to_boolean(row[1]),
            allow_hr_prop_emails            = utils.genesis_to_boolean(row[2]),
            allow_hr_update                 = utils.genesis_to_boolean(row[3]),
            period_to_overwrite_section     = utils.genesis_to_boolean(row[4]),
            prior_date_hr_to_post_daily     = utils.genesis_to_boolean(row[5]),
            allow_gb_update_all_grades      = utils.genesis_to_boolean(row[6]),
            allow_gb_update_fg              = utils.genesis_to_boolean(row[7]),
            alternate_code                  = row[8],
            is_alternate_program            = utils.genesis_to_boolean(row[9]),
            building_code                   = row[10],
            ceeb_code                       = row[11],
            is_charter_school               = utils.genesis_to_boolean(row[12]),
            is_choice                       = utils.genesis_to_boolean(row[13]),
            collect_ood_nj_smart_students   = utils.genesis_to_boolean(row[14]),
            school_count_students           = utils.genesis_to_boolean(row[15]),
            created_by_portal_oid           = row[16],
            created_by_task_oid             = row[17],
            created_by_user_oid             = row[18],
            created_ip                      = row[19],
            created_on                      = utils.genesis_to_datetime(row[20]),
            default_schedule_view           = row[21],
            is_esy_school                   = utils.genesis_to_boolean(row[22]),
            exclude_prek_njsmart_state      = utils.genesis_to_boolean(row[23]),
            exclude_reged_prek_njsmart      = utils.genesis_to_boolean(row[24]),
            excluded_school_from_njassa     = utils.genesis_to_boolean(row[25]),
            excluded_school_from_njsmart    = utils.genesis_to_boolean(row[26]),
            excluded_from_state_sped        = utils.genesis_to_boolean(row[27]),
            fall_eligibility_credits        = row[28],
            fall_eligibility_cred2014       = row[29],
            federal_school_code             = row[30],
            for_parents_module              = utils.genesis_to_boolean(row[31]),
            gen_pins_on_registration        = utils.genesis_to_boolean(row[32]),
            schedule_print_hide_bus         = utils.genesis_to_boolean(row[33]),
            highlight_dup_requests          = utils.genesis_to_boolean(row[34]),
            honor_rolls                     = row[35],
            hr_assignment_type              = row[36],
            hr_period                       = row[37],
            hr_period2                      = row[38],
            hr_period3                      = row[39],
            is_inact                        = utils.genesis_to_boolean(row[40]),
            in_district                     = utils.genesis_to_boolean(row[41]),
            word_day_in_bell                = utils.genesis_to_boolean(row[42]),
            keep_x_ny_sched_runs            = row[43],
            last_updated_by_portal_oid      = row[44],
            last_updated_by_task_oid        = row[45],
            last_updated_by_user_oid        = row[46],
            last_updated_ip                 = row[47],
            last_updated                    = utils.genesis_to_datetime(row[48]),
            locker_combination_cycle        = row[49],
            lock_hr_class_from_daily_prop   = utils.genesis_to_boolean(row[50]),
            non_public_school               = utils.genesis_to_boolean(row[51]),
            override_password               = row[52],
            pre_eval_school                 = utils.genesis_to_boolean(row[53]),
            is_prereg                       = utils.genesis_to_boolean(row[54]),
            prereg_school_code              = row[55],
            school_primary_color            = row[56],
            is_private_school_disabled      = utils.genesis_to_boolean(row[57]),
            regional_hs                     = utils.genesis_to_boolean(row[58]),
            rollover_ny_couns               = utils.genesis_to_boolean(row[59]),
            rollover_ny_hr                  = utils.genesis_to_boolean(row[60]),
            rollover_home_school            = utils.genesis_to_boolean(row[61]),
            rollover_res_school             = utils.genesis_to_boolean(row[62]),
            rollover_set_grad_date          = utils.genesis_to_boolean(row[63]),
            schedule_cycle_days             = row[64],
            schedule_cycle_days2            = row[65],
            schedule_cycle_naming           = row[66],
            schedule_cycle_naming2          = row[67],
            school_address1                 = row[68],
            school_address2                 = row[69],
            school_city                     = row[70],
            state_code                      = row[71],
            school_zipcode                  = row[72],
            school_category                 = row[73],
            school_code                     = row[74],
            school_contact_name             = row[75],
            school_description              = row[76],
            school_email                    = row[77],
            school_end_date                 = utils.genesis_to_date(row[78]),
            school_is_copy_of               = row[79],
            school_name                     = row[80],
            school_number                   = row[81],
            school_office_ext               = row[82],
            school_office_fax               = row[83],
            school_office_phone             = row[84],
            school_principal                = row[85],
            school_principal_email          = row[86],
            school_principal_ext            = row[87],
            school_principal_fax            = row[88],
            school_principal_phone          = row[89],
            school_special_designation      = row[90],
            school_start_date               = utils.genesis_to_date(row[91]),
            school_sys_admin                = row[92],
            school_sys_admin_email          = row[93],
            school_sys_admin_ext            = row[94],
            school_sys_admin_fax            = row[95],
            school_sys_admin_phone          = row[96],
            school_type_code                = row[97],
            school_url                      = row[98],
            school_year                     = row[99],
            school_secondary_color          = row[100],
            school_seq                      = row[101],
            all_schools_on_bell             = utils.genesis_to_boolean(row[102]),
            show_gb_district_proj_fg        = utils.genesis_to_boolean(row[103]),
            show_gb_projected_fg            = utils.genesis_to_boolean(row[104]),
            sif_id                          = row[105],
            speced_readonly                 = utils.genesis_to_boolean(row[106]),
            spring_eligibility_credits      = row[107],
            spring_eligibility_cred2014     = row[108],
            state_county_code               = row[109],
            state_district_code             = row[110],
            state_school_code               = row[111],
            student_id_counter              = row[112],
            student_pass_distribution       = row[113],
            att_checkin_pass_location       = row[114],
            att_checkin_pass                = utils.genesis_to_boolean(row[115]),
            student_pass_sort               = row[116],
            att_checkin_pass_reason         = row[117],
            student_sched_by_sem            = utils.genesis_to_boolean(row[118]),
            is_summer_school                = utils.genesis_to_boolean(row[119]),
            title_1_school                  = utils.genesis_to_boolean(row[120]),
            transcript_school_code          = row[121],
            random_bell_times               = utils.genesis_to_boolean(row[122]),
            update_hr_from_sched_screen     = utils.genesis_to_boolean(row[123]),
            use_gb_grade_for_auto_calc      = utils.genesis_to_boolean(row[124]),
            use_homeschool_assa             = utils.genesis_to_boolean(row[125]),
            att_checkin_use_minipass        = utils.genesis_to_boolean(row[126]),
            use_subsection_descriptions     = utils.genesis_to_boolean(row[127]),
            is_vocational                   = utils.genesis_to_boolean(row[128])
        )

    def __repr__(self):
        return 'School school_code={} school_name={}'.format(self.school_code, self.school_name)
