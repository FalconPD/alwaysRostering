from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from AR.tables.resident_district_tracking import ResidentDistrictTracking
from AR.tables.student_elem_homeroom import StudentElementaryHomeroom
from AR.tables.student_schedule import StudentSchedule
from AR.tables.student_user_text import StudentUserText
from AR.tables.students import Student
from AR.tables.staff_employment_record import StaffEmploymentRecord
from AR.tables.district_teacher import DistrictTeacher
from AR.tables.school_teacher import SchoolTeacher
from AR.tables.gradebook_teacher_section import GradebookTeacherSection
from AR.tables.school import School
from AR.tables.staff_job_roles import StaffJobRole
from AR.tables.master_class_schedule import CourseSection
from AR.tables.school_curriculum import CurriculumCourse
from AR.tables.master_class_subsections import CourseSubsection

sa_classes = [
    ResidentDistrictTracking,
    StudentElementaryHomeroom,
    StudentSchedule,
    Student,
    StudentUserText,
    DistrictTeacher,
    GradebookTeacherSection,
    School,
    SchoolTeacher,
    StaffJobRole,
    CurriculumCourse,
    CourseSection,
    CourseSubsection,
    StaffEmploymentRecord,
]
