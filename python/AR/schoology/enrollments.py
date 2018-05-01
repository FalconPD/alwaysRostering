"""Functions relating to enrollments"""

def create_object(section_school_code, school_uid, admin=False, delete=False):
    """Creats an enrollment object for use in
    course_enrollment_import_alternative"""

    enrollment = {
        'section_school_code': section_school_code,
        'school_uid': school_uid
    }
    if admin:
        enrollment['admin'] = '1'
    if delete:
        enrollment['delete'] = '1'
    return enrollment
