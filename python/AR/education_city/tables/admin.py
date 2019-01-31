import sqlalchemy
from sqlalchemy import Column, String
from AR.education_city.tables import Base

class Admin(Base):
    """
    This class represents an administrator in Education City
    """
    __tablename__ = 'Admin'

    Title       = Column(String)
    FirstName   = Column(String)
    LastName    = Column(String)
    Username    = Column(String, primary_key=True)
    Password    = Column(String)
    Email       = Column(String)

    csv_header = [
        'Title',
        'First Name',
        'Last Name',
        'Username',
        'Password',
        'Email',
        '', # EC seems to add an empty field in the response
    ]

    @classmethod
    def from_csv(cls, row):
        """
        Factory function for a Teacher from the CSV row
        """
        return cls(
            Title       = row[0],
            FirstName   = row[1],
            LastName    = row[2],
            Username    = row[3],
            Password    = row[4],
            Email       = row[5],
        )

    def __repr__(self):
        return (f"Admin FirstName={self.FirstName} LastName={self.LastName}"
            f"Username={self.Username}")
