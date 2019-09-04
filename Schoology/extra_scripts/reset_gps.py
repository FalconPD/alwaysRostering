"""
Looks up all of the 2018-19 courses in Genesis and resets their
grading_period to 'All Year 2018-19' in Schoology
"""

# In our python environment
import asyncio
import sys

# In the alwaysRostering environment
import AR.AR as AR
from AR.tables import CurriculumCourse, CourseSection
import AR.schoology as schoology

# Local
sys.path.append('..')
import utils

# Get all of last year's sections
AR.init("../../databases/2019-09-02-full-genesis.db")
sections = (
    AR.db_session.query(CurriculumCourse)
    .filter(CurriculumCourse.course_code != '000')
    .filter(CurriculumCourse.school_code.in_(AR.school_codes))
    .filter(CurriculumCourse.sections.any(CourseSection.assigned_seats > 0))
    .filter(CurriculumCourse.school_year == '2018-19')
    .join(CourseSection)
    .filter(CourseSection.assigned_seats > 0)
    .with_entities(CourseSection)
)
for section in sections:
    if section.merged:
        print(section)
        print(section.school_year)
        print(section.section_school_code)
