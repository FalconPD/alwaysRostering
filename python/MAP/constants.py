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
    'BES': (
        '140', # Mathematics
        '150', # Mathematics
        '159', # Accelerated Math
        '240', # English Language Arts
        '250', # English Language Arts
    ),
    'MTHS': (
        '0707',     # Algebra I A/B
        '0708',     # Algebra I
        '0709',     # Geometry
        '0710',     # Algebra II
        '0716',     # Honors Geometry
        '0717',     # Honors Algebra II
        '0717STEM', # Honors Algebra II
        '0721',     # Dynamics of Trig/Math
        '0723',     # Dynamics of Geometry
        '0724',     # Dynamics of Algebra II
        '0728',     # Precalculus
        '0729',     # Honors Precalculus
        '0729STEM', # H Precalculus
        '0730',     # Honors Calculus
        '0731',     # Probability & Statistics
        '0732',     # Advanced Placement Statistics
        '0734',     # Advanced Placement Calculus BC
        '0735',     # Advanced Placement Calculus AB
        '0739',     # Advanced Placement Calculus AB/BC
        '0601',     # Language Arts I
        '0602',     # Honors Language Arts 1
        '0603',     # Language Arts II
        '0604',     # Honors Language Arts II
        '0604STEM', # Honors Language Arts II
        '0606',     # Language Arts III
        '0607',     # Honors Language Arts III
        '0607STEM', # Honors Language Arts III
        '0620',     # Advanced Placement Language Arts III
        '0624',     # Honors World Studies Language Arts
        '0625',     # Honors American Studies I Language
        '0626',     # Honors American Studies 2 Language
        '1312',     # Math/Dynamics of Geometry
        '1313',     # Math/Dynamics of Algebra II
        '1317',     # Reading
        '1318',     # Language Arts 9 (Resource)
        '1319',     # Language Arts 10
        '1320',     # Language Arts 11
        '1321',     # Language Arts 12
        '1325',     # Math/Dynamics of Algebra I
        '1332',     # Math IV Computers in Business
        '1342',     # Algebra I A/B
        '1343',     # Dynamics of Algebra II
        '1351',     # Language Arts III (ICR) 
        '1355',     # Langauge Arts I (ICR)
        '1368',     # Language Arts IV Contemp Iss/Mon Lit
        '1369',     # Language Arts IV Pop Culture
        '1380',     # Dynamics of Geom
        '1381',     # Geometry
        '1382',     # Algebra II
        '1383',     # Algebra I
        '1390',     # Math For Real Life
        '1407',     # Algebra I
        '1408',     # Geometry
        '1409',     # Algebra II
        '1419',     # Language Arts (MAPS)
        '1611',     # Fundamentals of Geometry
        '1619',     # Language Arts
        '1700',     # Vocational Exploration
        '1701',     # Functional Academics
        '1702',     # Life Skills
    ),
    'MTMS': (
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
    'WES': (
        '140', # Mathematics
        '150', # Mathematics
        '159', # Accelerated Mathematics
        '240', # English Language Arts
        '250', # English Language Arts
    ),
}

SCREENING_PROCTORS = {
    'BBS': ('5030', '629', '5074'),
    'MLS': ('443', '476', '404'),
    'OTS': ('5457', '667', '5076'),
}

EXTRA_CLASSES = {
    'OT (Unrostered in Genesis)': {
        'teacher_id': '586',
        'student_ids': ('92170', '89897', '89900', '91303', '92518')
    }, 
    'ELA (Unrostered in Genesis)': {
        'teacher_id': '603',
        'student_ids': ('89662', '92433', '91570', '91931', '90638')
    },
    'Math (Unrostered in Genesis)': {
        'teacher_id': '603',
        'student_ids': ('89662', '92433', '91570', '90638', '89695')
    },
}

DUPLICATES = {
    '8204': ('6843',),
    '6621': ('6309',),
    '6662': ('6309',),
    '6655': ('6309',),
    '6539': ('569',),
    '6314': ('569',),    
}
