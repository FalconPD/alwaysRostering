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

AR.init('../databases/2019-04-08-genesis.db')

# Roster 3-5
print("Rostering grades 3-5...")
with open('3-5.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    grade_levels = ['03', '04', '05']
    students = AR.students().filter(Student.grade_level.in_(grade_levels))
    for student in students:
        row = {}
        row['School Name (Required)']                      = student.school.school_name
        row['School ID Number (Optional)']                 = student.school.school_code
        row['Student First Name (Required)']               = student.first_name
        row['Student Last Name (Required)']                = student.last_name
        row['Student ID Number (Required)']                = student.student_id
        row['Student Grade Level (Required)']              = student.grade_level
        row['Student Gender (Optional)']                   = student.gender
        row['Student Race (Optional)']                     = student.race
        row['Student FRPL Status (Optional)']              = student.free_or_reduced_lunch
        row['Student ELL Status (Optional)']               = 'FIXME'
        row['Student Gifted Status (Optional)']            = student.gifted_talented
        row['Student Special Education Status (Optional)'] = student.spec_ed
        row['Course Section Name (Optional)']              = student.homeroom_name 
        row['Course Section Period (Optional)']            = ''
        for teacher in student.homeroom_teachers:
            row['Employee First Name (Optional)'] = teacher.teacher_first_name
            row['Employee Last Name (Optional)']  = teacher.teacher_last_name
            row['Employee ID Number (Optional)']  = teacher.teacher_id
            row['Employee Email (Optional)']      = teacher.email
            row['Employee Gender (Optional)']     = teacher.gender_code
            writer.writerow(row)
