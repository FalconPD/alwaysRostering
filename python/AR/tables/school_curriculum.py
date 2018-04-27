from sqlalchemy import Column, Integer, String, Boolean, BigInteger, Date, DateTime, Float
from sqlalchemy.orm import relationship
from AR.tables import Base
from AR.tables import utils
import re
import logging

class CurriculumCourse(Base):
    __tablename__ = 'SCHOOL_CURRICULUM'

    is_academic = Column('IS_ACADEMIC', Boolean, nullable=False)
    accelerated = Column('ACCELERATED', Boolean, nullable=False)
    advanced_level = Column('ADVANCED_LEVEL', Boolean, nullable=False)
    advanced_placement_course = Column('ADVANCED_PLACEMENT_COURSE', Boolean, nullable=False)
    assign_room = Column('ASSIGN_ROOM', Boolean, nullable=False)
    assign_teacher = Column('ASSIGN_TEACHER', Boolean, nullable=False)
    attendance_taken = Column('ATTENDANCE_TAKEN', Boolean, nullable=False)
    biology_type = Column('BIOLOGY_TYPE', String(50))
    cip_code = Column('CIP_CODE', String(6))
    collects_comments = Column('COLLECTS_COMMENTS', Boolean, nullable=False)
    collects_overall_grade = Column('COLLECTS_OVERALL_GRADE', Boolean, nullable=False)
    college_prep_course = Column('COLLEGE_PREP_COURSE', Boolean, nullable=False)
    core_course_flag = Column('CORE_COURSE_FLAG', String(8))
    core_subject = Column('CORE_SUBJECT', String(25))
    course_active = Column('COURSE_ACTIVE', Boolean, nullable=False)
    course_adoption_date = Column('COURSE_ADOPTION_DATE', Date)
    course_catalog_description = Column('COURSE_CATALOG_DESCRIPTION', String(4000))
    course_code = Column('COURSE_CODE', String(25), primary_key=True, nullable=False)
    course_credits = Column('COURSE_CREDITS', Float, nullable=False)
    course_curriculum = Column('COURSE_CURRICULUM', String(30))
    course_description = Column('COURSE_DESCRIPTION', String(50), nullable=False)
    course_length = Column('COURSE_LENGTH', String(2))
    course_level = Column('COURSE_LEVEL', String(100))
    course_level_code = Column('COURSE_LEVEL_CODE', String(8))
    course_req_subject_area_code = Column('COURSE_REQ_SUBJECT_AREA_CODE', String(8))
    course_type = Column('COURSE_TYPE', String(10))
    crdc_classification = Column('CRDC_CLASSIFICATION', String(100))
    created_by_portal_oid = Column('CREATED_BY_PORTAL_OID', BigInteger)
    created_by_task_oid = Column('CREATED_BY_TASK_OID', BigInteger)
    created_by_user_oid = Column('CREATED_BY_USER_OID', BigInteger)
    created_ip = Column('CREATED_IP', String(100))
    created_on = Column('CREATED_ON', DateTime)
    curriculum_adoption_date = Column('CURRICULUM_ADOPTION_DATE', Date)
    custom_data_1 = Column('CUSTOM_DATA_1', String(255))
    cycle_set = Column('CYCLE_SET', Integer, nullable=False)
    default_seats = Column('DEFAULT_SEATS', Integer, nullable=False)
    department_code = Column('DEPARTMENT_CODE', String(8))
    display_in_parents_as_gb = Column('DISPLAY_IN_PARENTS_AS_GB', Boolean, nullable=False)
    display_in_parents_schedgrade = Column('DISPLAY_IN_PARENTS_SCHEDGRADE', Boolean, nullable=False)
    is_elective = Column('IS_ELECTIVE', Boolean, nullable=False)
    elementary_course = Column('ELEMENTARY_COURSE', Boolean, nullable=False)
    elem_fg_skill_code = Column('ELEM_FG_SKILL_CODE', String(50))
    exclude_from_njsmart = Column('EXCLUDE_FROM_NJSMART', Boolean, nullable=False)
    course_flag1 = Column('COURSE_FLAG1', Boolean, nullable=False)
    course_flag2 = Column('COURSE_FLAG2', Boolean, nullable=False)
    course_flag3 = Column('COURSE_FLAG3', Boolean, nullable=False)
    course_flag4 = Column('COURSE_FLAG4', Boolean, nullable=False)
    global_course_alternate = Column('GLOBAL_COURSE_ALTERNATE', String(10))
    gpa_level = Column('GPA_LEVEL', Integer)
    gpa_weight = Column('GPA_WEIGHT', Float, nullable=False)
    gpa_weight_alpha = Column('GPA_WEIGHT_ALPHA', BigInteger)
    gpa_weight_code = Column('GPA_WEIGHT_CODE', String(8))
    gpa_weight_code_alpha = Column('GPA_WEIGHT_CODE_ALPHA', String(8))
    gpa_weight_code_numeric = Column('GPA_WEIGHT_CODE_NUMERIC', String(8))
    gpa_weight_numeric = Column('GPA_WEIGHT_NUMERIC', BigInteger)
    graded_course = Column('GRADED_COURSE', Boolean, nullable=False)
    health_course_code = Column('HEALTH_COURSE_CODE', String(25))
    honors_course = Column('HONORS_COURSE', Boolean, nullable=False)
    ignore_sced_for_parcc = Column('IGNORE_SCED_FOR_PARCC', Boolean, nullable=False)
    ignore_restrictions = Column('IGNORE_RESTRICTIONS', Boolean, nullable=False)
    include_in_gpa = Column('INCLUDE_IN_GPA', Boolean, nullable=False)
    include_in_honor_roll = Column('INCLUDE_IN_HONOR_ROLL', Boolean, nullable=False)
    include_on_transcript = Column('INCLUDE_ON_TRANSCRIPT', Boolean, nullable=False)
    inclusion_course_code_link = Column('INCLUSION_COURSE_CODE_LINK', String(10))
    inclusion_course_option = Column('INCLUSION_COURSE_OPTION', String(50))
    instruction_type_code = Column('INSTRUCTION_TYPE_CODE', String(3))
    lab_before_or_after = Column('LAB_BEFORE_OR_AFTER', Boolean, nullable=False)
    last_updated_by_portal_oid = Column('LAST_UPDATED_BY_PORTAL_OID', BigInteger)
    last_updated_by_task_oid = Column('LAST_UPDATED_BY_TASK_OID', BigInteger)
    last_updated_by_user_oid = Column('LAST_UPDATED_BY_USER_OID', BigInteger)
    last_updated_ip = Column('LAST_UPDATED_IP', String(100))
    last_updated = Column('LAST_UPDATED', DateTime)
    legacy_course_code = Column('LEGACY_COURSE_CODE', String(50))
    linked_sem_course_sections = Column('LINKED_SEM_COURSE_SECTIONS', Boolean, nullable=False)
    linked_sem_courses = Column('LINKED_SEM_COURSES', String(25))
    lunch_flag = Column('LUNCH_FLAG', Boolean, nullable=False)
    max_requests = Column('MAX_REQUESTS', Integer)
    maximum_seats = Column('MAXIMUM_SEATS', Integer, nullable=False)
    minutes_per_week = Column('MINUTES_PER_WEEK', Integer)
    ncaa_core_course = Column('NCAA_CORE_COURSE', Boolean, nullable=False)
    next_course_code = Column('NEXT_COURSE_CODE', String(50))
    next_school_code = Column('NEXT_SCHOOL_CODE', String(50))
    num_days_for_course = Column('NUM_DAYS_FOR_COURSE', Integer)
    num_days_for_lab = Column('NUM_DAYS_FOR_LAB', Integer)
    num_sections = Column('NUM_SECTIONS', Integer)
    parents_can_request = Column('PARENTS_CAN_REQUEST', Boolean, nullable=False)
    periods_per_day = Column('PERIODS_PER_DAY', Integer)
    phys_ed_course = Column('PHYS_ED_COURSE', Boolean, nullable=False)
    planned_eval_date = Column('PLANNED_EVAL_DATE', Date)
    pre_requisites = Column('PRE_REQUISITES', Boolean, nullable=False)
    pre_sec_sced_course_code = Column('PRE_SEC_SCED_COURSE_CODE', String(5))
    primary_subject_area_code = Column('PRIMARY_SUBJECT_AREA_CODE', String(8))
    readoption_date = Column('READOPTION_DATE', Date)
    sced_course_code = Column('SCED_COURSE_CODE', String(5))
    sced_course_level = Column('SCED_COURSE_LEVEL', String(1))
    sced_grade_span = Column('SCED_GRADE_SPAN', String(4))
    sced_sequence = Column('SCED_SEQUENCE', String(2))
    scheduling_priority = Column('SCHEDULING_PRIORITY', Integer, nullable=False)
    school_code = Column('SCHOOL_CODE', String(8), primary_key=True, nullable=False)
    school_year = Column('SCHOOL_YEAR', String(7), primary_key=True, nullable=False)
    secondary_subject_area_code = Column('SECONDARY_SUBJECT_AREA_CODE', String(8))
    sem_avail = Column('SEM_AVAIL', String(3))
    short_description = Column('SHORT_DESCRIPTION', String(15))
    sif_id = Column('SIF_ID', String(32))
    sif_subject_area = Column('SIF_SUBJECT_AREA', String(3))
    sif_subject_area2 = Column('SIF_SUBJECT_AREA2', String(3))
    skill_group = Column('SKILL_GROUP', String(15))
    special_ed_course = Column('SPECIAL_ED_COURSE', Boolean, nullable=False)
    special_program_desc = Column('SPECIAL_PROGRAM_DESC', String(4000))
    state_course_code = Column('STATE_COURSE_CODE', String(50))
    state_test_1 = Column('STATE_TEST_1', String(50))
    state_test_2 = Column('STATE_TEST_2', String(50))
    study_hall_flag = Column('STUDY_HALL_FLAG', Boolean, nullable=False)
    team_code = Column('TEAM_CODE', String(8))
    tech_prep = Column('TECH_PREP', Boolean, nullable=False)

    sections = relationship('CourseSection', back_populates='course') 

    report_code = '991067'
    csv_header = [ 
        'IS_ACADEMIC',
        'ACCELERATED',
        'ADVANCED_LEVEL',
        'ADVANCED_PLACEMENT_COURSE',
        'ASSIGN_ROOM',
        'ASSIGN_TEACHER',
        'ATTENDANCE_TAKEN',
        'BIOLOGY_TYPE',
        'CIP_CODE',
        'COLLECTS_COMMENTS',
        'COLLECTS_OVERALL_GRADE',
        'COLLEGE_PREP_COURSE',
        'CORE_COURSE_FLAG',
        'CORE_SUBJECT',
        'COURSE_ACTIVE',
        'COURSE_ADOPTION_DATE',
        'COURSE_CATALOG_DESCRIPTION',
        'COURSE_CODE',
        'COURSE_CREDITS',
        'COURSE_CURRICULUM',
        'COURSE_DESCRIPTION',
        'COURSE_LENGTH',
        'COURSE_LEVEL',
        'COURSE_LEVEL_CODE',
        'COURSE_REQ_SUBJECT_AREA_CODE',
        'COURSE_TYPE',
        'CRDC_CLASSIFICATION',
        'CREATED_BY_PORTAL_OID',
        'CREATED_BY_TASK_OID',
        'CREATED_BY_USER_OID',
        'CREATED_IP',
        'CREATED_ON',
        'CURRICULUM_ADOPTION_DATE',
        'CUSTOM_DATA_1',
        'CYCLE_SET',
        'DEFAULT_SEATS',
        'DEPARTMENT_CODE',
        'DISPLAY_IN_PARENTS_AS_GB',
        'DISPLAY_IN_PARENTS_SCHEDGRADE',
        'IS_ELECTIVE',
        'ELEMENTARY_COURSE',
        'ELEM_FG_SKILL_CODE',
        'EXCLUDE_FROM_NJSMART',
        'COURSE_FLAG1',
        'COURSE_FLAG2',
        'COURSE_FLAG3',
        'COURSE_FLAG4',
        'GLOBAL_COURSE_ALTERNATE',
        'GPA_LEVEL',
        'GPA_WEIGHT',
        'GPA_WEIGHT_ALPHA',
        'GPA_WEIGHT_CODE',
        'GPA_WEIGHT_CODE_ALPHA',
        'GPA_WEIGHT_CODE_NUMERIC',
        'GPA_WEIGHT_NUMERIC',
        'GRADED_COURSE',
        'HEALTH_COURSE_CODE',
        'HONORS_COURSE',
        'IGNORE_SCED_FOR_PARCC',
        'IGNORE_RESTRICTIONS',
        'INCLUDE_IN_GPA',
        'INCLUDE_IN_HONOR_ROLL',
        'INCLUDE_ON_TRANSCRIPT',
        'INCLUSION_COURSE_CODE_LINK',
        'INCLUSION_COURSE_OPTION',
        'INSTRUCTION_TYPE_CODE',
        'LAB_BEFORE_OR_AFTER',
        'LAST_UPDATED_BY_PORTAL_OID',
        'LAST_UPDATED_BY_TASK_OID',
        'LAST_UPDATED_BY_USER_OID',
        'LAST_UPDATED_IP',
        'LAST_UPDATED',
        'LEGACY_COURSE_CODE',
        'LINKED_SEM_COURSE_SECTIONS',
        'LINKED_SEM_COURSES',
        'LUNCH_FLAG',
        'MAX_REQUESTS',
        'MAXIMUM_SEATS',
        'MINUTES_PER_WEEK',
        'NCAA_CORE_COURSE',
        'NEXT_COURSE_CODE',
        'NEXT_SCHOOL_CODE',
        'NUM_DAYS_FOR_COURSE',
        'NUM_DAYS_FOR_LAB',
        'NUM_SECTIONS',
        'PARENTS_CAN_REQUEST',
        'PERIODS_PER_DAY',
        'PHYS_ED_COURSE',
        'PLANNED_EVAL_DATE',
        'PRE_REQUISITES',
        'PRE_SEC_SCED_COURSE_CODE',
        'PRIMARY_SUBJECT_AREA_CODE',
        'READOPTION_DATE',
        'SCED_COURSE_CODE',
        'SCED_COURSE_LEVEL',
        'SCED_GRADE_SPAN',
        'SCED_SEQUENCE',
        'SCHEDULING_PRIORITY',
        'SCHOOL_CODE',
        'SCHOOL_YEAR',
        'SECONDARY_SUBJECT_AREA_CODE',
        'SEM_AVAIL',
        'SHORT_DESCRIPTION',
        'SIF_ID',
        'SIF_SUBJECT_AREA',
        'SIF_SUBJECT_AREA2',
        'SKILL_GROUP',
        'SPECIAL_ED_COURSE',
        'SPECIAL_PROGRAM_DESC',
        'STATE_COURSE_CODE',
        'STATE_TEST_1',
        'STATE_TEST_2',
        'STUDY_HALL_FLAG',
        'TEAM_CODE',
        'TECH_PREP',
    ]

    @classmethod
    def from_csv(cls, row):
        return cls(
            is_academic                     = utils.genesis_to_boolean(row[0]),
            accelerated                     = utils.genesis_to_boolean(row[1]),
            advanced_level                  = utils.genesis_to_boolean(row[2]),
            advanced_placement_course       = utils.genesis_to_boolean(row[3]),
            assign_room                     = utils.genesis_to_boolean(row[4]),
            assign_teacher                  = utils.genesis_to_boolean(row[5]),
            attendance_taken                = utils.genesis_to_boolean(row[6]),
            biology_type                    = row[7],
            cip_code                        = row[8],
            collects_comments               = utils.genesis_to_boolean(row[9]),
            collects_overall_grade          = utils.genesis_to_boolean(row[10]),
            college_prep_course             = utils.genesis_to_boolean(row[11]),
            core_course_flag                = row[12],
            core_subject                    = row[13],
            course_active                   = utils.genesis_to_boolean(row[14]),
            course_adoption_date            = utils.genesis_to_date(row[15]),
            course_catalog_description      = row[16],
            course_code                     = row[17],
            course_credits                  = row[18],
            course_curriculum               = row[19],
            course_description              = row[20],
            course_length                   = row[21],
            course_level                    = row[22],
            course_level_code               = row[23],
            course_req_subject_area_code    = row[24],
            course_type                     = row[25],
            crdc_classification             = row[26],
            created_by_portal_oid           = row[27],
            created_by_task_oid             = row[28],
            created_by_user_oid             = row[29],
            created_ip                      = row[30],
            created_on                      = utils.genesis_to_datetime(row[31]),
            curriculum_adoption_date        = utils.genesis_to_date(row[32]),
            custom_data_1                   = row[33],
            cycle_set                       = row[34],
            default_seats                   = row[35],
            department_code                 = row[36],
            display_in_parents_as_gb        = utils.genesis_to_boolean(row[37]),
            display_in_parents_schedgrade   = utils.genesis_to_boolean(row[38]),
            is_elective                     = utils.genesis_to_boolean(row[39]),
            elementary_course               = utils.genesis_to_boolean(row[40]),
            elem_fg_skill_code              = row[41],
            exclude_from_njsmart            = utils.genesis_to_boolean(row[42]),
            course_flag1                    = utils.genesis_to_boolean(row[43]),
            course_flag2                    = utils.genesis_to_boolean(row[44]),
            course_flag3                    = utils.genesis_to_boolean(row[45]),
            course_flag4                    = utils.genesis_to_boolean(row[46]),
            global_course_alternate         = row[47],
            gpa_level                       = row[48],
            gpa_weight                      = row[49],
            gpa_weight_alpha                = row[50],
            gpa_weight_code                 = row[51],
            gpa_weight_code_alpha           = row[52],
            gpa_weight_code_numeric         = row[53],
            gpa_weight_numeric              = row[54],
            graded_course                   = utils.genesis_to_boolean(row[55]),
            health_course_code              = row[56],
            honors_course                   = utils.genesis_to_boolean(row[57]),
            ignore_sced_for_parcc           = utils.genesis_to_boolean(row[58]),
            ignore_restrictions             = utils.genesis_to_boolean(row[59]),
            include_in_gpa                  = utils.genesis_to_boolean(row[60]),
            include_in_honor_roll           = utils.genesis_to_boolean(row[61]),
            include_on_transcript           = utils.genesis_to_boolean(row[62]),
            inclusion_course_code_link      = row[63],
            inclusion_course_option         = row[64],
            instruction_type_code           = row[65],
            lab_before_or_after             = utils.genesis_to_boolean(row[66]),
            last_updated_by_portal_oid      = row[67],
            last_updated_by_task_oid        = row[68],
            last_updated_by_user_oid        = row[69],
            last_updated_ip                 = row[70],
            last_updated                    = utils.genesis_to_datetime(row[71]),
            legacy_course_code              = row[72],
            linked_sem_course_sections      = utils.genesis_to_boolean(row[73]),
            linked_sem_courses              = row[74],
            lunch_flag                      = utils.genesis_to_boolean(row[75]),
            max_requests                    = row[76],
            maximum_seats                   = row[77],
            minutes_per_week                = row[78],
            ncaa_core_course                = utils.genesis_to_boolean(row[79]),
            next_course_code                = row[80],
            next_school_code                = row[81],
            num_days_for_course             = row[82],
            num_days_for_lab                = row[83],
            num_sections                    = row[84],
            parents_can_request             = utils.genesis_to_boolean(row[85]),
            periods_per_day                 = row[86],
            phys_ed_course                  = utils.genesis_to_boolean(row[87]),
            planned_eval_date               = utils.genesis_to_date(row[88]),
            pre_requisites                  = utils.genesis_to_boolean(row[89]),
            pre_sec_sced_course_code        = row[90],
            primary_subject_area_code       = row[91],
            readoption_date                 = utils.genesis_to_date(row[92]),
            sced_course_code                = row[93],
            sced_course_level               = row[94],
            sced_grade_span                 = row[95],
            sced_sequence                   = row[96],
            scheduling_priority             = row[97],
            school_code                     = row[98],
            school_year                     = row[99],
            secondary_subject_area_code     = row[100],
            sem_avail                       = row[101],
            short_description               = row[102],
            sif_id                          = row[103],
            sif_subject_area                = row[104],
            sif_subject_area2               = row[105],
            skill_group                     = row[106],
            special_ed_course               = utils.genesis_to_boolean(row[107]),
            special_program_desc            = row[108],
            state_course_code               = row[109],
            state_test_1                    = row[110],
            state_test_2                    = row[111],
            study_hall_flag                 = utils.genesis_to_boolean(row[112]),
            team_code                       = row[113],
            tech_prep                       = utils.genesis_to_boolean(row[114])
        )

    def __repr__(self):
        return '{} {} {}'.format(self.school_code, self.course_code, self.course_description)
