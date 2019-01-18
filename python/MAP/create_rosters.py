import csv
import logging
import click
import constants
from sqlalchemy import or_, and_

import AR.AR as AR
from AR.tables import CurriculumCourse, DistrictTeacher, School, Student
from AR.tables import SchoolTeacher, CourseSection

standard_roster = None
additional_users = None
teachers = set()

def add_school_to_row(row, school):
    """
    Adds information from a School to the CSV row
    """
    row['School State Code'] = school.state_school_code
    row['School Name']       = school.school_name
    return row

def add_teacher_to_row(row, district_teacher):
    """
    Adds information from a DistrictTeacher to the CSV row
    """
    global teachers

    teachers.add(district_teacher)
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
    """
    Adds information from a Student to the CSV row
    """
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

def roster_k3():
    """
    roster grades K-3 and programs by HR teacher
    """
    grade_levels = ['KH', 'KF', '01', '02', '03']

    # certain programs in certain buildings also need to be rostered by HR
    school_codes = ['BES', 'BBS', 'OTS', 'MLS']
    program_types = ['23', '30'] # Multiple Disabilities, Autism

    students = (AR.students()
        .filter(
            or_(
                Student.grade_level.in_(grade_levels),
                and_(
                    Student.current_program_type_code.in_(program_types),
                    Student.current_school.in_(school_codes),
                ),
            )
        )
    )
    print("Rostering {} grade K-3 students by HR teacher...".format(
        students.count()))
    for student in students:
        for teacher in student.homeroom_teachers:
            row = add_school_to_row({}, student.school)
            row['Class Name'] = 'Homeroom ' + student.homeroom_suffix
            row = add_teacher_to_row(row, teacher)
            row = add_student_to_row(row, student)
            standard_roster.writerow(row)
            if teacher.teacher_id in constants.DUPLICATES:
                row['Class Name'] += ' ' + teacher.teacher_last_name
                for additional_teacher_id in constants.DUPLICATES[teacher.teacher_id]:
                    additional_teacher = (AR.teachers()
                        .filter(DistrictTeacher.teacher_id==additional_teacher_id)
                        .one()
                    )
                    row = add_teacher_to_row(row, additional_teacher)
                    standard_roster.writerow(row)

    print("Rostering K-3 classes that aren't in Genesis...")
    for class_name, class_info in constants.EXTRA_CLASSES.items(): 
        teacher =  (AR.teachers()
            .filter(DistrictTeacher.teacher_id==class_info['teacher_id'])
            .one()
        )
        print("* {} {}".format(class_name, teacher))
        for student_id in class_info['student_ids']:
            student = (AR.students()
                .filter(Student.student_id==student_id)
                .one()
            )
            row = add_school_to_row({}, student.school)
            row['Class Name'] = class_name
            row = add_teacher_to_row(row, teacher)
            row = add_student_to_row(row, student)
            standard_roster.writerow(row)

def roster_screening():
    """
    roster pre-registered students for screening
    """
    print("Rostering students for kindergarten screening...")
    students = (AR.db_session.query(Student)
        .filter(Student.current_school=='PREG')
        .filter(
            or_(
                Student.grade_level=='KH',
                Student.grade_level=='KF',
            )
        )
    )
    for student in students:
        # If a preregistrant has resident_district_tracking, use it to figure
        # out what school they are going in to. If not, use home_school in
        # Student. Otherwise, skip.
        if student.resident_district_tracking:
            code = student.resident_district_tracking.resident_school_code
            if code == '010':
                school_code = 'BBS'
            elif code == '040':
                school_code = 'MLS'
            elif code == '060':
                school_code = 'OTS'
            else:
                logging.warning("Can't map {} to school_code for {}".format(
                    code, student))
        else:
            logging.warning(
                "No entry in Resident District Tracking for {}".format(student))
            if student.home_school:
                school_code = student.home_school
            else:
                logging.warning(
                    "home_school not set for {}, skipping".format(student))
                continue
        proctors = constants.SCREENING_PROCTORS[school_code]
        school = AR.schools().filter(School.school_code==school_code).one()
        row = {
            'Class Name': 'Kindergarten Screening ' + school.school_name
        }
        row = add_school_to_row(row, school)
        row = add_student_to_row(row, student)
        row['Student Grade'] = 'PK'
        for teacher_id in proctors:
            teacher = (AR.staff()
                .filter(DistrictTeacher.teacher_id==teacher_id)
                .one()
            )
            row = add_teacher_to_row(row, teacher)
            standard_roster.writerow(row)

def roster_412():
    """
    roster grades 4-12 by course
    """
    print("Rostering grade 4-12 students by course...")
    for school_code, course_codes in constants.SCHOOL_COURSE_CODES.items():
        school = AR.schools().filter(School.school_code==school_code).one()
        print("{}".format(school.school_name))
        row=add_school_to_row({}, school)
        courses = (AR.courses()
            .filter(CurriculumCourse.school_code==school.school_code)
            .filter(CurriculumCourse.course_code.in_(course_codes))
        )
        for course in courses:
            print("* {} {}".format(course.course_code,
                course.course_description))
            for section in course.active_sections:
                row['Class Name'] = section.name
                teacher_id = section.first_subsection.teacher_id
                query = (AR.teachers()
                    .filter(DistrictTeacher.teacher_id==teacher_id)
                )
                if query.count() != 1:
                    print("Unable to lookup teacher_id: {} for section: {}"
                        .format(teacher_id, section))
                    continue
                district_teacher = query.one()
                row = add_teacher_to_row(row, district_teacher)
                for student in section.active_students:
                    row = add_student_to_row(row, student)
                    standard_roster.writerow(row)
                # Also add students from any merged sections
                if section.merged:
                    for section in section.merged_sections:
                        for student in section.active_students:
                            row = add_student_to_row(row, student)
                            standard_roster.writerow(row)

    print("Adding 5th grade Accelerated Math students to HR teacher's math class...")
    for section in AR.sections().filter(CourseSection.course_code=="159"):
        for student in section.active_students:
            for teacher in student.homeroom_teachers:
                for hr_math_section in AR.sections().filter(CourseSection.course_code=="150"):
                    if hr_math_section.first_subsection.teacher_id == teacher.teacher_id:
                        school = AR.schools().filter(School.school_code==hr_math_section.school_code).one()
                        row = add_school_to_row({}, school)
                        row['Class Name'] = hr_math_section.name
                        row = add_teacher_to_row(row, teacher)
                        row = add_student_to_row(row, student)
                        standard_roster.writerow(row)

def users():
    """
    Creates the AdditionalUsers file based on all the teachers that have
    been referenced.
    """
    for teacher in teachers:
        row = {}
        row['School State Code']                       = ''
        row['School Name']                             = ''
        row['Instructor ID']                           = teacher.teacher_id
        row['Instructor State ID']                     = teacher.state_id_number
        row['Last Name']                               = teacher.last_name
        row['First Name']                              = teacher.first_name
        row['Middle Name']                         = teacher.teacher_middle_name
        row['User Name']                               = teacher.long_email
        row['Email Address']                           = teacher.long_email
        row['Role = School Proctor?']                  = 'Y'
        row['Role = School Assessment Coordinator?']   = ''
        row['Role = Administrator?']                   = ''
        row['Role = District Proctor?']                = ''
        row['Role = Data Administrator?']              = ''
        row['Role = District Assessment Coordinator?'] = ''
        row['Role = Interventionist?']                 = ''
        row['Role = SN Administrator?']                = ''
        additional_users.writerow(row)

@click.group(chain=True)
@click.option('--debug', help="turn on debugging", is_flag=True)
@click.argument('db_file', type=click.Path(exists=True))
@click.argument('prefix')
def cli(debug, db_file, prefix):
    """
    Loads a Genesis database from DB_FILE and performs COMMAND(s). Writes
    output files with the PREFIX specified.

    """
    global standard_roster
    global additional_users

    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    db_session = AR.init(db_file)

    # Temporary fixes for erroneous Genesis data

    # Invalid shared HR teacher at WES
    district_teacher = db_session.query(DistrictTeacher).filter(DistrictTeacher.teacher_id=="8211").one()
    district_teacher.shared_teacher = True
    district_teacher.shared_teacher_id_1 = "2108"
    district_teacher.shared_teacher_id_2 = "6943"
    
    output = prefix + '_StandardRoster.csv'
    csvfile = open(output, 'w', newline='')
    standard_roster = csv.DictWriter(csvfile,
        fieldnames=constants.STANDARDROSTER_FIELDNAMES)
    standard_roster.writeheader()

    output = prefix + '_AdditionalUsers.csv'
    csvfile = open(output, 'w', newline='')
    additional_users = csv.DictWriter(csvfile,
        fieldnames=constants.ADDITIONALUSERS_FIELDNAMES)
    additional_users.writeheader()

@cli.command(name="K-3")
def cli_roster_k3():
    """
    roster grades K-3 and programs by HR teacher
    """
    roster_k3()

@cli.command(name="4-12")
def cli_roster_412():
    """
    roster grades 4-12 by course
    """
    roster_412()

@cli.command(name="screening")
def cli_roster_screening():
    """
    roster students for kindergarten screening
    """
    roster_screening()

@cli.command(name="additional_users")
def cli_additional_users():
    """
    create AdditionalUsers file
    """
    users()

@cli.command()
def all():
    """
    perform all rostering commands
    """
    roster_k3()
    roster_412()
    roster_screening()
    users()

if __name__ == '__main__':
    cli()
