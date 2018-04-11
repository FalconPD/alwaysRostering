import logging
import argparse
import AR.AR as AR

parser = argparse.ArgumentParser(description='Build a MAP roster from Genesis reports')
parser.add_argument('-d', '--debug',
    help='print debugging statements',
    action='store_const',
    dest='loglevel',
    const=logging.DEBUG,
    default=logging.WARNING)
parser.add_argument('db_file',
    help='genesis database file to load (sqlite3)')
args = parser.parse_args()

logging.basicConfig(level=args.loglevel)
AR.init(args.db_file)

# The following is test code that was found in AR.py

# All the students we test and their classes
all_students = (
    db_session.query(Student, StudentSchedule)
    .outerjoin(StudentSchedule)
    .filter(Student.enrollment_status == 'ACTIVE')
    .filter(Student.homebound_status == 'NO')
    .filter(Student.grade_level.in_(['KH', 'KF', '01', '02', '03', '04', '05', '06', '07', '08']))
    .filter(Student.current_school.in_(['AES', 'AMS', 'BBS', 'BES', 'MLS', 'OTS', 'WES']))
)
all_ids = {student.student_id for student, cls in all_students}
print('Students to roster: {}'.format(len(all_ids)))

# Grades K-3 and certain programs are rostered by their HR teacher
hr_students = (
    all_students
    .distinct(Student.student_id) # there may be multiples if a student has two classes
    .filter(or_(
        Student.grade_level.in_(['KH', 'KF', '01', '02', '03']),
        Student.current_program_type_code.in_(['30', '23'])
    ))
)
for student, cls in hr_students:
    row = []
    row[0] = #School State Code
    row[1] = #School Name
    row[2] = #Previous Instructor ID
    row[3] = #Instructor ID
    row[4] = #Instructor State ID
    row[5] = #Instructor Last Name
    row[6] = #Instructor First Name
    row[7] = #Instructor Middle Initial
    row[8] = #User Name
    row[9] = #Email Address
    row[10] = #Class Name
    row[11] = #Previous Student ID
    row[12] = #Student ID
    row[13] = #Student State ID
    row[14] = #Student Last Name
    row[14] = #Student First Name
    row[15] = #Student Middle Initial
    row[16] = #Student Date Of Birth
    row[17] = #Student Gender
    row[18] = #Student Grade
    row[19] = #Student Ethnic Group Name
    row[20] = #Student User Name
    row[21] = #Student Email
hr_ids = {student.student_id for student, cls in hr_students}
print('Rostered by HR teacher: {}'.format(len(hr_ids)))

# Everybody else is rostered by their classes
cls_students = (
    all_students
    .except_(hr_students)
    .filter(or_(
        and_(StudentSchedule.school_code == 'AMS', StudentSchedule.course_code.in_(["105", "110", "111", "120", "160", "170", "180", "260", "270", "280"])),
        and_(StudentSchedule.school_code == 'AES', StudentSchedule.course_code.in_(["140", "150", "159", "201", "240", "250"])),
        and_(StudentSchedule.school_code == 'BES', StudentSchedule.course_code.in_(["140", "150", "159", "240", "250"])),
        and_(StudentSchedule.school_code == 'WES', StudentSchedule.course_code.in_(["140", "150", "159", "240", "250"]))
    ))
)
cls_ids = {student.student_id for student, cls in cls_students}
print('Uniqued students rostered by class: {}'.format(len(cls_ids)))

# There should be no overlap between our two lists
print('Overlap: {}'.format(hr_ids & cls_ids))
print('Not rostered: {}'.format(all_ids - hr_ids - cls_ids))

