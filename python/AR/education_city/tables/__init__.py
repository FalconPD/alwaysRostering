from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from AR.education_city.tables.student import Student
from AR.education_city.tables.teacher import Teacher
from AR.education_city.tables.admin import Admin
