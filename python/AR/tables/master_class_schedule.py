from sqlalchemy import Column, Integer, String, Boolean, BigInteger, DateTime, Float, ForeignKeyConstraint, or_
from sqlalchemy.orm import relationship, object_session
from AR.tables import Base
from AR.tables import utils
from AR.tables import GradebookTeacherSection
import logging

class CourseSection(Base):
    __tablename__ = 'MASTER_CLASS_SCHEDULE'
    __table_args__ = (
        ForeignKeyConstraint(
            [
                'SCHOOL_YEAR',
                'SCHOOL_CODE',
                'COURSE_CODE'
            ],
            [
                'SCHOOL_CURRICULUM.SCHOOL_YEAR',
                'SCHOOL_CURRICULUM.SCHOOL_CODE',
                'SCHOOL_CURRICULUM.COURSE_CODE'
            ]
        ),
    )

    assigned_seats = Column('ASSIGNED_SEATS', Integer, nullable=False)
    attendance_taken = Column('ATTENDANCE_TAKEN', Boolean, nullable=False)
    available_seats = Column('AVAILABLE_SEATS', Integer, nullable=False)
    beginning_seats = Column('BEGINNING_SEATS', Integer, nullable=False)
    course_code = Column('COURSE_CODE', String(25), primary_key=True, nullable=False)
    course_section = Column('COURSE_SECTION', Integer, primary_key=True, nullable=False)
    created_by_portal_oid = Column('CREATED_BY_PORTAL_OID', BigInteger)
    created_by_task_oid = Column('CREATED_BY_TASK_OID', BigInteger)
    created_by_user_oid = Column('CREATED_BY_USER_OID', BigInteger)
    created_ip = Column('CREATED_IP', String(100))
    created_on = Column('CREATED_ON', DateTime)
    cycle_code = Column('CYCLE_CODE', String(1))
    cycle_set = Column('CYCLE_SET', Integer, nullable=False)
    fg_collected_in = Column('FG_COLLECTED_IN', String(4))
    gpa_weight = Column('GPA_WEIGHT', Float, nullable=False)
    gpa_weight_code = Column('GPA_WEIGHT_CODE', String(8))
    graded_course = Column('GRADED_COURSE', Boolean, nullable=False)
    homeroom = Column('HOMEROOM', String(25))
    include_in_gpa = Column('INCLUDE_IN_GPA', Boolean, nullable=False)
    include_in_honor_roll = Column('INCLUDE_IN_HONOR_ROLL', Boolean, nullable=False)
    include_on_transcript = Column('INCLUDE_ON_TRANSCRIPT', Boolean, nullable=False)
    instruction_type_code = Column('INSTRUCTION_TYPE_CODE', String(3))
    last_updated_by_portal_oid = Column('LAST_UPDATED_BY_PORTAL_OID', BigInteger)
    last_updated_by_task_oid = Column('LAST_UPDATED_BY_TASK_OID', BigInteger)
    last_updated_by_user_oid = Column('LAST_UPDATED_BY_USER_OID', BigInteger)
    last_updated_ip = Column('LAST_UPDATED_IP', String(100))
    last_updated = Column('LAST_UPDATED', DateTime)
    legacy_course_code = Column('LEGACY_COURSE_CODE', String(255))
    legacy_course_section = Column('LEGACY_COURSE_SECTION', String(255))
    mp_credits = Column('MP_CREDITS', Float)
    next_gen_class = Column('NEXT_GEN_CLASS', String(20))
    override_seats = Column('OVERRIDE_SEATS', Integer, nullable=False)
    parcc_test_code = Column('PARCC_TEST_CODE', String(20))
    receiving_school = Column('RECEIVING_SCHOOL', String(8))
    sced_course_code = Column('SCED_COURSE_CODE', String(5))
    sced_course_level = Column('SCED_COURSE_LEVEL', String(1))
    sced_grade_span = Column('SCED_GRADE_SPAN', String(4))
    sced_sequence = Column('SCED_SEQUENCE', String(2))
    schedule_description = Column('SCHEDULE_DESCRIPTION', String(50))
    scheduling_shift = Column('SCHEDULING_SHIFT', Integer, nullable=False)
    school_code = Column('SCHOOL_CODE', String(8), primary_key=True, nullable=False)
    school_year = Column( 'SCHOOL_YEAR', String(7), primary_key=True, nullable=False)
    shared_class = Column('SHARED_CLASS', String(8))
    skill_group = Column('SKILL_GROUP', String(15))
    suppress_from_report_card = Column('SUPPRESS_FROM_REPORT_CARD', Boolean, nullable=False)
    team_code = Column('TEAM_CODE', String(100))
    total_mp_grades_collected = Column('TOTAL_MP_GRADES_COLLECTED', Integer, nullable=False)
    transcript_description = Column('TRANSCRIPT_DESCRIPTION', String(30))
    use_in_parcc = Column('USE_IN_PARCC', Boolean, nullable=False)

    course = relationship('CurriculumCourse', back_populates='sections')
    subsections = relationship('CourseSubsection', back_populates='section')
    gb_teacher_sections = relationship('GradebookTeacherSection', back_populates='section')

    report_code = '991073'
    csv_header = [ 
        'ASSIGNED_SEATS',
        'ATTENDANCE_TAKEN',
        'AVAILABLE_SEATS',
        'BEGINNING_SEATS',
        'COURSE_CODE',
        'COURSE_SECTION',
        'CREATED_BY_PORTAL_OID',
        'CREATED_BY_TASK_OID',
        'CREATED_BY_USER_OID',
        'CREATED_IP',
        'CREATED_ON',
        'CYCLE_CODE',
        'CYCLE_SET',
        'FG_COLLECTED_IN',
        'GPA_WEIGHT',
        'GPA_WEIGHT_CODE',
        'GRADED_COURSE',
        'HOMEROOM',
        'INCLUDE_IN_GPA',
        'INCLUDE_IN_HONOR_ROLL',
        'INCLUDE_ON_TRANSCRIPT',
        'INSTRUCTION_TYPE_CODE',
        'LAST_UPDATED_BY_PORTAL_OID',
        'LAST_UPDATED_BY_TASK_OID',
        'LAST_UPDATED_BY_USER_OID',
        'LAST_UPDATED_IP',
        'LAST_UPDATED',
        'LEGACY_COURSE_CODE',
        'LEGACY_COURSE_SECTION',
        'MP_CREDITS',
        'NEXT_GEN_CLASS',
        'OVERRIDE_SEATS',
        'PARCC_TEST_CODE',
        'RECEIVING_SCHOOL',
        'SCED_COURSE_CODE',
        'SCED_COURSE_LEVEL',
        'SCED_GRADE_SPAN',
        'SCED_SEQUENCE',
        'SCHEDULE_DESCRIPTION',
        'SCHEDULING_SHIFT',
        'SCHOOL_CODE',
        'SCHOOL_YEAR',
        'SHARED_CLASS',
        'SKILL_GROUP',
        'SUPPRESS_FROM_REPORT_CARD',
        'TEAM_CODE',
        'TOTAL_MP_GRADES_COLLECTED',
        'TRANSCRIPT_DESCRIPTION',
        'USE_IN_PARCC'
    ]

    @classmethod
    def from_csv(cls, row):
        return cls(
            assigned_seats              = row[0],
            attendance_taken            = utils.genesis_to_boolean(row[1]),
            available_seats             = row[2],
            beginning_seats             = row[3],
            course_code                 = row[4],
            course_section              = row[5],
            created_by_portal_oid       = row[6],
            created_by_task_oid         = row[7],
            created_by_user_oid         = row[8],
            created_ip                  = row[9],
            created_on                  = utils.genesis_to_datetime(row[10]),
            cycle_code                  = row[11],
            cycle_set                   = row[12],
            fg_collected_in             = row[13],
            gpa_weight                  = row[14],
            gpa_weight_code             = row[15],
            graded_course               = utils.genesis_to_boolean(row[16]),
            homeroom                    = row[17],
            include_in_gpa              = utils.genesis_to_boolean(row[18]),
            include_in_honor_roll       = utils.genesis_to_boolean(row[19]),
            include_on_transcript       = utils.genesis_to_boolean(row[20]),
            instruction_type_code       = row[21],
            last_updated_by_portal_oid  = row[22],
            last_updated_by_task_oid    = row[23],
            last_updated_by_user_oid    = row[24],
            last_updated_ip             = row[25],
            last_updated                = utils.genesis_to_datetime(row[26]),
            legacy_course_code          = row[27],
            legacy_course_section       = row[28],
            mp_credits                  = utils.genesis_to_nullable_float(row[29]),
            next_gen_class              = row[30],
            override_seats              = row[31],
            parcc_test_code             = row[32],
            receiving_school            = row[33],
            sced_course_code            = row[34],
            sced_course_level           = row[35],
            sced_grade_span             = row[36],
            sced_sequence               = row[37],
            schedule_description        = row[38],
            scheduling_shift            = row[39],
            school_code                 = row[40],
            school_year                 = row[41],
            shared_class                = row[42],
            skill_group                 = row[43],
            suppress_from_report_card   = utils.genesis_to_boolean(row[44]),
            team_code                   = row[45],
            total_mp_grades_collected   = row[46],
            transcript_description      = row[47],
            use_in_parcc                = utils.genesis_to_boolean(row[48])
        )
    
    @property
    def first_active_gb_teacher_section(self):
        """Finds the FIRST active gradebook for this section"""

        for gb_teacher_section in self.gb_teacher_sections:
            if gb_teacher_section.active == True:
                return gb_teacher_section
        return None

    @property
    def gb_course_id(self):
        """Returns the course_id for the FIRST active gradebook for this section"""

        gb_teacher_section = self.first_active_gb_teacher_section
        if gb_teacher_section != None:
            return gb_teacher_section.course_id
        return None

    @property
    def merged(self):
        """Tells you whether this section has a merged gradebook with another
        section"""

        gb_teacher_section = self.first_active_gb_teacher_section
        if gb_teacher_section != None:
            return gb_teacher_section.merged
        return False

    @property
    def merged_sections(self):
        """Returns a list of all the sections that share an active, merged
        gradebook with this section. Merged sections DO NOT have to have the
        same course_code."""

        merged_sections = []
        query = (
            object_session(self)
            .query(GradebookTeacherSection)
            .filter(self.school_year == GradebookTeacherSection.school_year)
            .filter(self.school_code == GradebookTeacherSection.school_code)
            .filter(self.gb_course_id == GradebookTeacherSection.course_id)
            .filter(GradebookTeacherSection.active == True)
            .filter(or_(self.course_section != GradebookTeacherSection.course_section,
                self.course_code != GradebookTeacherSection.course_code)) # filter out ourself
        )
        for gb_teacher_section in query:
            merged_sections.append(gb_teacher_section.section)
        return merged_sections

    @property
    def first_subsection(self):
        if (len(self.subsections) == 0):
            logging.warning('{}: No subsections'.format(self))
            return None
        elif (len(self.subsections) > 1):
            # NOTE: It seems subsections are used to split up a course by
            # marking period in gym
            logging.warning('{}: Multiple subsections, using first'.format(self))
        return self.subsections[0]

    @property
    def day(self):
        """Gets the meeting day(s) from the first subsection"""

        if self.first_subsection != None:
            if self.first_subsection.meets_cycles != '':
                return self.first_subsection.meets_cycles
        logging.warning('{}: Unable to lookup day'.format(self))
        return None

    @property
    def period(self):
        """Gets the meeting period(s) from the first subsection"""

        if self.first_subsection != None:
            if self.first_subsection.print_period != '':
                return self.first_subsection.print_period
        logging.warning('{}: Unable to lookup period'.format(self))
        return None

    @property
    def name(self):
        """Returns a friendly name for the course section depending on your
        school. Should end up being the same for merged courses."""

        if self.school_code == 'MTHS':
            return '{}{} {}'.format(self.period, self.day,
                self.course.course_description)
        return '{} {} {}'.format(self.course_code, self.course_section,
            self.course.course_description)

    @property
    def section_school_code(self):
        """Returns an identifier unique across the whole district. Merged
        courses should get the same result.
        
        Format: <School Code> [(<Course Code 1>, <Course Section 1>), ...]"""

        course_sections = ['({}, {})'.format(
            self.course_code,
            self.course_section
        )]
        if self.merged:
            for merged_section in self.merged_sections:
                course_sections.append('({}, {})'.format(
                    merged_section.course_code,
                    merged_section.course_section
                ))

        return '{} {}'.format(
            self.school_code, 
            ', '.join(sorted(course_sections))
        )

    def __repr__(self):
        return (
            'CourseSection '
            'school_code={} '
            'course_code={} '
            'course_section={} '
            'course_description={}'
        ).format(
            self.school_code,
            self.course_code,
            self.course_section,
            self.schedule_description
        )
