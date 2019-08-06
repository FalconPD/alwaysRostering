import sqlalchemy
from sqlalchemy import Column, Integer, String, Boolean, Date
from AR.PG.tables import Base
from AR.PG.tables.utils import to_datetime

class UserProfile(Base):
    __tablename__ = 'UserProfile'

    UserID                      = Column(Integer, primary_key=True)
    FirstName                   = Column(String)
    LastName                    = Column(String)
    UserName                    = Column(String)
    Email                       = Column(String)
    EmployeeID                  = Column(String)
    DistrictID                  = Column(Integer)
    EmailNotification           = Column(Boolean)
    JobTitle                    = Column(String)
    LastLoginDate               = Column(Date)
    IsInstructor                = Column(Boolean)
    IsDistrictAdmin             = Column(Boolean)
    IsHighlyQualified           = Column(Boolean)
    PositionType                = Column(String)
    IsCertified                 = Column(Boolean)
    StateCertificateID          = Column(String)
    CertificateExpirationDate   = Column(Date)
    Active                      = Column(Boolean)
    DateAdded                   = Column(Date)
    DateHired                   = Column(Date)
    DateTerminated              = Column(Date)

    @classmethod
    def from_row(cls, row, datemode):
        """
        Factory function for a UserProfile from the xlrd row
        """
        return cls(
            UserID                      = int(row[0].value),
            FirstName                   = row[1].value,
            LastName                    = row[2].value,
            UserName                    = row[3].value,
            Email                       = row[4].value,
            EmployeeID                  = row[5].value,
            DistrictID                  = int(row[6].value),
            EmailNotification           = bool(row[7].value),
            JobTitle                    = row[8].value,
            LastLoginDate               = to_datetime(row[9], datemode),
            IsInstructor                = bool(row[10].value),
            IsDistrictAdmin             = bool(row[11].value),
            IsHighlyQualified           = bool(row[12].value),
            PositionType                = row[13].value,
            IsCertified                 = bool(row[14].value),
            StateCertificateID          = row[15].value,
            CertificateExpirationDate   = to_datetime(row[16], datemode),
            Active                      = bool(row[17].value),
            DateAdded                   = to_datetime(row[18], datemode),
            DateHired                   = to_datetime(row[19], datemode),
            DateTerminated              = to_datetime(row[20], datemode),
        )

    def __repr__(self):
        return "UserProfile UserID={} EmployeeID={} FirstName={} LastName={}".format(
            self.UserID, self.EmployeeID, self.FirstName, self.LastName)
