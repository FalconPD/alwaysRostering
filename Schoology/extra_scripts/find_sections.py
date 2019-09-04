import csv
import re
import AR.AR as AR
from AR.tables import CourseSection

AR.init("../../databases/2019-09-02-full-genesis.db")

counts = {}
with open('2019-20_enrollments.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        section_school_code = row['Section School Code']
        status = row['Status']
        enrollment_type = row['Enrollment Type (1=Admin/2=Member)']
        if section_school_code not in counts:
            counts[section_school_code] = 0
        if status == '1' and enrollment_type == '1':
            counts[section_school_code] += 1

# Find all sections that don't have admins
for section_school_code, count in counts.items():
    if count < 1:
        # Get their course_code and course_section from the schoology 'Section School Code'
        matches = re.match(r'([A-Z]+?) (\(.*?\))(, )?(\(.*?\))?', section_school_code)
        school_code = matches.group(1)
        course_section1 = matches.group(2)
        course_section2 = matches.group(4)
        matches = re.match(r'\(([0-9A-Z]+), ([0-9A-Z]+)\)', course_section1)
        course_code1 = matches.group(1)
        course_section1 = matches.group(2)
        if course_section2 != None:
            matches = re.match(r'\(([0-9A-Z]+), ([0-9A-Z]+)\)', course_section2)
            course_code2 = matches.group(1)
            course_section2 = matches.group(2)

        # Lookup the teacher IDs for this course in 2018-19
        teacher_id1 = None
        section = (
            AR.db_session.query(CourseSection)
            .filter(CourseSection.school_code==school_code)
            .filter(CourseSection.school_year=='2018-19')
            .filter(CourseSection.course_code==course_code1)
            .filter(CourseSection.course_section==course_section1)
            .one_or_none()
        )
        if section != None:
            teacher_id1 = section.first_subsection.teacher_id

        teacher_id2 = None
        if course_section2 != None:
            section = (
                AR.db_session.query(CourseSection)
                .filter(CourseSection.school_code==school_code)
                .filter(CourseSection.school_year=='2018-19')
                .filter(CourseSection.course_code==course_code2)
                .filter(CourseSection.course_section==course_section2)
                .one_or_none()
            )
            if section != None:
                teacher_id2 = section.first_subsection.teacher_id

        print(f"\"{school_code} {course_code1}\",\"{section_school_code}\",\"{teacher_id1}\"")
        if teacher_id2 != None:
            print(f"\"{school_code} {course_code2}\",\"{section_school_code}\",\"{teacher_id2}\"")
