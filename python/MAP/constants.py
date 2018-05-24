STANDARDROSTER_FIELDNAMES = (
    'School State Code',
    'School Name',
    'Previous Instructor ID',
    'Instructor ID',
    'Instructor State ID',
    'Instructor Last Name',
    'Instructor First Name',
    'Instructor Middle Initial',
    'User Name',
    'Email Address',
    'Class Name',
    'Previous Student ID',
    'Student ID',
    'Student State ID',
    'Student Last Name',
    'Student First Name',
    'Student Middle Initial',
    'Student Date Of Birth',
    'Student Gender',
    'Student Grade',
    'Student Ethnic Group Name',
    'Student User Name',
    'Student Email',
)

ADDITIONALUSERS_FIELDNAMES = (
    'School State Code',
    'School Name',
    'Instructor ID',
    'Instructor State ID',
    'Last Name',
    'First Name',
    'Middle Name',
    'User Name',
    'Email Address',
    'Role = School Proctor?',
    'Role = School Assessment Coordinator?',
    'Role = Administrator?',
    'Role = District Proctor?',
    'Role = Data Administrator?',
    'Role = District Assessment Coordinator?',
    'Role = Interventionist?',
    'Role = SN Administrator?',
)

SCHOOL_COURSE_CODES = {
    'AES': (
        '140', # Mathematics
        '150', # Mathematics
        '159', # Accelerated Math
        '201', # Wilson Reading
        '240', # English Language Arts 
        '250', # English Language Arts
    ),
    'AMS': (
        '105', # Accelerated Math
        '110', # Algebra I
        '111', # Accelerated Algebra I
        '120', # Geometry
        '160', # Mathematics - Sixth Grade
        '170', # Mathematics - Seventh Grade
        '180', # Mathematics - Eight Grade
        '260', # Language Arts - Sixth Grade
        '270', # Language Arts - Seventh Grade
        '280', # Langauge Arts - Eight Grade 
    ),
    'BES': (
        '140', # Mathematics
        '150', # Mathematics
        '159', # Accelerated Math
        '240', # English Language Arts
        '250', # English Language Arts
    ),
    'WES': (
        '140', # Mathematics
        '150', # Mathematics
        '159', # Accelerated Mathematics
        '240', # English Language Arts
        '250', # English Language Arts
    ),
}
