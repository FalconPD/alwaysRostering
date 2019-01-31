import sqlalchemy
from sqlalchemy import Column, Integer, String, Date
from AR.education_city.tables import Base
# Education City and Genesis use the same data format
from AR.tables.utils import genesis_to_date as to_date
from AR.tables import Student as GenesisStudent

class Student(Base):
    __tablename__ = 'Student'

    UniqueID        = Column(Integer, primary_key=True)
    FirstName       = Column(String)
    LastName        = Column(String)
    ClassName       = Column(String)
    Username        = Column(String)
    Password        = Column(String)
    Gender          = Column(String)
    DateOfBirth     = Column(Date)
    AcademicLevel   = Column(String)
    LastUpdated     = Column(Date)

    csv_header = [
        'Unique ID',
        'First Name',
        'Last Name',
        'Class Name',
        'Username',
        'Password',
        'Gender',
        'Date of Birth',
        'Academic Level',
        'Last Updated',
        '', # seems to add an empty field in the response
    ]

    @classmethod
    def from_genesis(cls, genesis_student):
        """
        Factory function for a Student from a Genesis Student
        """
        return cls(
            UniqueID        = genesis_student.student_id,
            FirstName       = genesis_student.first_name,
            LastName        = genesis_student.last_name,
            ClassName       = genesis_student.homeroom_name,
            Username        = genesis_student.simple_username,
            Password        = genesis_student.simple_password,
            Gender          = genesis_student.gender.lower(),
            DateOfBirth     = genesis_student.date_of_birth,
            AcademicLevel   = genesis_student.academic_level,
        )

    @classmethod
    def from_csv(cls, row):
        """
        Factory function for a Student from the CSV row
        """
        return cls(
            UniqueID        = row[0],
            FirstName       = row[1],
            LastName        = row[2],
            ClassName       = row[3],
            Username        = row[4],
            Password        = row[5],
            Gender          = row[6],
            DateOfBirth     = to_date(row[7]),
            AcademicLevel   = row[8],
            LastUpdated     = to_date(row[9]),
        )

    def __repr__(self):
        return (f"Student UniqueID={self.UniqueID} FirstName={self.FirstName} "
                f"LastName={self.LastName}")
