import csv
import logging
import click
import constants

import sys
sys.path.append("..")
import AR.AR as AR
from AR.tables import CurriculumCourse, DistrictTeacher, School

def add_teacher_to_row(row, district_teacher):
    row['Previous Instructor ID']    = ""
    row['Instructor ID']             = district_teacher.teacher_id
    row['Instructor State ID']       = district_teacher.state_id_number
    row['Instructor Last Name']      = district_teacher.last_name
    row['Instructor First Name']     = district_teacher.first_name
    row['Instructor Middle Initial'] = district_teacher.teacher_middle_name
    row['User Name']                 = district_teacher.long_email
    row['Email Address']             = district_teacher.long_email
    return row

def add_student_to_row(row, student):
    row['Previous Student ID'] = ""
    row['Student ID'] = student.student_id
    row['Student State ID'] = student.state_id_number
    row['Student Last Name'] = student.last_name
    row['Student First Name'] = student.first_name
    row['Student Middle Initial'] = student.middle_name
    row['Student Date Of Birth'] = student.date_of_birth
    row['Student Gender'] = student.gender
    row['Student Grade'] = student.grade
    row['Student Ethnic Group Name'] = student.race
    row['Student User Name'] = student.email
    row['Student Email'] = student.email
    return row

@click.command()
@click.option('--debug', help="turn on debugging", is_flag=True)
@click.argument('db_file', type=click.Path(exists=True))
@click.argument('output', type=click.Path(writable=True))
def main(debug, db_file, output):
    """
    Creates MAP rosters.
    Loads a Genesis database from DB_FILE and saves the roster to OUTPUT
    """
    if debug:
        logging.basicConfig(logging.DEBUG)
    else:
        logging.basicConfig()

    AR.init(db_file)

    with open(output, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=constants.FIELDNAMES)
        writer.writeheader()

        row={}
        school = AR.schools().filter(School.school_code=='AMS').one()
        row['School State Code'] = school.state_school_code
        row['School Name']       = school.school_name
        course_codes = constants.COURSE_CODES[school.school_code]
        courses = (AR.courses()
            .filter(CurriculumCourse.school_code==school.school_code)
            .filter(CurriculumCourse.course_code.in_(course_codes))
        )
        print(course_codes)
        for course in courses:
            for section in course.sections:
                row['Class Name'] = section.name
                teacher_id = section.first_subsection.teacher_id
                district_teacher = (AR.teachers()
                    .filter(DistrictTeacher.teacher_id==teacher_id)
                    .one()
                )
                row = add_teacher_to_row(row, district_teacher)
                for student in section.active_students:
                    row = add_student_to_row(row, student)
                    writer.writerow(row)
                # Also add students from any merged sections
                if section.merged:
                    for section in section.merged_sections:
                        for student in section.active_students:
                            row = add_student_to_row(row, student)
                            writer.writerow(row)

if __name__ == '__main__':
    main()

# The following is test code that was found in AR.py

# All the students we test and their classes
#all_students = (
#    db_session.query(Student, StudentSchedule)
#    .outerjoin(StudentSchedule)
#    .filter(Student.enrollment_status == 'ACTIVE')
#    .filter(Student.homebound_status == 'NO')
#    .filter(Student.grade_level.in_(['KH', 'KF', '01', '02', '03', '04', '05', '06', '07', '08']))
#    .filter(Student.current_school.in_(['AES', 'AMS', 'BBS', 'BES', 'MLS', 'OTS', 'WES']))
#)
#all_ids = {student.student_id for student, cls in all_students}
#print('Students to roster: {}'.format(len(all_ids)))
#
## Grades K-3 and certain programs are rostered by their HR teacher
#hr_students = (
#    all_students
#    .distinct(Student.student_id) # there may be multiples if a student has two classes
#    .filter(or_(
#        Student.grade_level.in_(['KH', 'KF', '01', '02', '03']),
#        Student.current_program_type_code.in_(['30', '23'])
#    ))
#)
#for student, cls in hr_students:
#    row = []
#    row[0] = #School State Code
#    row[1] = #School Name
#    row[2] = #Previous Instructor ID
#    row[3] = #Instructor ID
#    row[4] = #Instructor State ID
#    row[5] = #Instructor Last Name
#    row[6] = #Instructor First Name
#    row[7] = #Instructor Middle Initial
#    row[8] = #User Name
#    row[9] = #Email Address
#    row[10] = #Class Name
#    row[11] = #Previous Student ID
#    row[12] = #Student ID
#    row[13] = #Student State ID
#    row[14] = #Student Last Name
#    row[14] = #Student First Name
#    row[15] = #Student Middle Initial
#    row[16] = #Student Date Of Birth
#    row[17] = #Student Gender
#    row[18] = #Student Grade
#    row[19] = #Student Ethnic Group Name
#    row[20] = #Student User Name
#    row[21] = #Student Email
#hr_ids = {student.student_id for student, cls in hr_students}
#print('Rostered by HR teacher: {}'.format(len(hr_ids)))

# Everybody else is rostered by their classes
#cls_students = (
#    all_students
#    .except_(hr_students)
#    .filter(or_(
#        and_(StudentSchedule.school_code == 'AMS', StudentSchedule.course_code.in_(["105", "110", "111", "120", "160", "170", "180", "260", "270", "280"])),
#        and_(StudentSchedule.school_code == 'AES', StudentSchedule.course_code.in_(["140", "150", "159", "201", "240", "250"])),
#        and_(StudentSchedule.school_code == 'BES', StudentSchedule.course_code.in_(["140", "150", "159", "240", "250"])),
#        and_(StudentSchedule.school_code == 'WES', StudentSchedule.course_code.in_(["140", "150", "159", "240", "250"]))
#    ))
#)
#cls_ids = {student.student_id for student, cls in cls_students}
#print('Uniqued students rostered by class: {}'.format(len(cls_ids)))

# There should be no overlap between our two lists
#print('Overlap: {}'.format(hr_ids & cls_ids))
#print('Not rostered: {}'.format(all_ids - hr_ids - cls_ids))
