import csv
import logging

import AR.AR as AR
from AR.tables import Student, School

fieldnames = [
    "School Name (Required)",
    "School ID Number (Optional)",
    "Course Section Name (Optional)",
    "Course Section Period (Optional)",
    "Employee First Name (Optional)",
    "Employee Last Name (Optional)",
    "Employee ID Number (Optional)",
    "Employee Email (Optional)",
    "Employee Gender (Optional)",
    "Student First Name (Required)",
    "Student Last Name (Required)",
    "Student ID Number (Required)",
    "Student Grade Level (Required)",
    "Student Gender (Optional)",
    "Student Race (Optional)",
    "Student FRPL Status (Optional)",
    "Student ELL Status (Optional)",
    "Student Gifted Status (Optional)",
    "Student Special Education Status (Optional)",
]

def add_school_info(school, row={}):
    """
    Adds the school information to a row
    """    
    row['School Name (Required)']      = school.school_name
    row['School ID Number (Optional)'] = school.school_code
    return row
        
def add_student_info(student, row={}):
    """
    Adds the student information to a row
    """    
    row['Student First Name (Required)']               = student.first_name
    row['Student Last Name (Required)']                = student.last_name
    row['Student ID Number (Required)']                = student.student_id
    row['Student Grade Level (Required)']              = student.grade
    row['Student Gender (Optional)']                   = student.gender
    row['Student Race (Optional)']                     = student.race
    row['Student FRPL Status (Optional)']              = 'Yes' if student.free_or_reduced_lunch else 'No'
    row['Student ELL Status (Optional)']               = 'ELL' if student.ell else ''
    row['Student Gifted Status (Optional)']            = 'Yes' if student.gifted_talented else 'No'
    row['Student Special Education Status (Optional)'] = 'Yes' if student.spec_ed == 'YES' else 'No'
    return row

def add_teacher_info(teacher, row={}):
    """
    Adds the teacher information to a row
    """    
    row['Employee First Name (Optional)'] = '' if teacher == None else teacher.teacher_first_name
    row['Employee Last Name (Optional)']  = '' if teacher == None else teacher.teacher_last_name
    row['Employee ID Number (Optional)']  = '' if teacher == None else teacher.teacher_id
    row['Employee Email (Optional)']      = '' if teacher == None else teacher.email
    row['Employee Gender (Optional)']     = '' if teacher == None else teacher.gender_code
    return row

AR.init('../databases/2019-04-10-genesis.db')

print("Rostering grades all grades...")
with open('roster.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Roster 3-5
    grade_levels = ['03', '04', '05']
    students = AR.students().filter(Student.grade_level.in_(grade_levels))
    for student in students:
        row = add_school_info(student.school)
        row = add_student_info(student, row)
        row['Course Section Name (Optional)']   = student.homeroom_name 
        row['Course Section Period (Optional)'] = ''
        for teacher in student.homeroom_teachers:
            row = add_teacher_info(teacher, row)
            writer.writerow(row)

    # Roster 6-12
    grade_levels = ['06', '07', '08', '09', '10', '11', '12']
    students = AR.students().filter(Student.grade_level.in_(grade_levels))
    for student in students:
        row = add_school_info(student.school)
        row = add_student_info(student, row)
        for schedule in student.student_schedules:
            if schedule.course_status == 'ACTIVE':
                # Include ICR and Regular Ed teachers
                all_sections = ([schedule.section] +
                    schedule.section.merged_sections)
                for section in all_sections:
                    row['Course Section Name (Optional)']   = section.name
                    row['Course Section Period (Optional)'] = ''
                    teacher = section.first_subsection.teacher
                    # Some courses like Early Out, don't have teachers
                    # MTMS Uses the teacher STAFF, STAFF (genesis id 257) for
                    # lunches
                    if teacher != None and teacher.teacher_id != '257':
                        row = add_teacher_info(teacher, row)
                        writer.writerow(row)
