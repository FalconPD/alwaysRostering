import sqlalchemy
from sqlalchemy import Column, Integer, String, Boolean, Date, Numeric, Float
from decimal import Decimal
from AR.PG.tables import Base
from AR.PG.tables.utils import to_datetime

class Activity(Base):
    __tablename__ = 'Activities'

    ActivityTitle       = Column(String)
    ActivityDesc        = Column(String)
    ActivityID          = Column(Integer, primary_key=True)
    DistrictID          = Column(Integer)
    ProviderID          = Column(Integer)
    ActivityFormatID    = Column(Integer)
    PaymentFormatID     = Column(Integer)
    CCatalogID          = Column(Integer)
    EventID             = Column(Integer)
    Type                = Column(String)
    InstructorUserID    = Column(Integer)
    InstructorName      = Column(String)
    PGDate              = Column(Date) # name had to be changed
    StartDate           = Column(Date)
    DateExpired         = Column(Date)
    MeetingDates        = Column(String)
    URL                 = Column(String)
    EndDate             = Column(Date)
    MaxUsers            = Column(Integer)
    Archived            = Column(Boolean)
    ApprovalRequired    = Column(Boolean)
    UserCanEdit         = Column(Boolean)
    ActivityHours       = Column(Float)
    QuickApprove        = Column(Boolean)
    Credits             = Column(Float)
    FormID              = Column(Integer)
    Comments            = Column(String)
    ConferenceLocation  = Column(String)
    Level               = Column(String)
    SubscriberFee       = Column(Numeric)
    NonSubscriberFee    = Column(Numeric)
    DateAdded           = Column(Date)
    DateUpdated         = Column(Date)
    ShowSubscriberFee   = Column(Boolean)
    StartShowing        = Column(Date)
    StopShowing         = Column(Date)

    @classmethod
    def from_row(cls, row, datemode):
        """
        Factory function for a Activity from the xlrd row
        """
        return cls(
            ActivityTitle = row[0].value,
            ActivityDesc = row[1].value,
            ActivityID = int(row[2].value),
            DistrictID = int(row[3].value),
            ProviderID = int(row[4].value),
            ActivityFormatID = int(row[5].value),
            PaymentFormatID = int(row[6].value),
            CCatalogID = int(row[7].value),
            EventID = int(row[8].value),
            Type= row[9].value,
            InstructorUserID = int(row[10].value),
            InstructorName = row[11].value,
            PGDate = to_datetime(row[12], datemode),
            StartDate = to_datetime(row[13], datemode),
            DateExpired = to_datetime(row[14], datemode),
            MeetingDates= row[15].value,
            URL= row[16].value,
            EndDate = to_datetime(row[17], datemode),
            MaxUsers = int(row[18].value),
            Archived = bool(row[19].value),
            ApprovalRequired = bool(row[20].value),
            UserCanEdit = bool(row[21].value),
            ActivityHours = float(row[22].value),
            QuickApprove = bool(row[23].value),
            Credits = float(row[24].value),
            FormID = int(row[25].value),
            Comments = row[26].value,
            ConferenceLocation = row[27].value,
            Level = row[28].value,
            SubscriberFee = Decimal(row[29].value),
            NonSubscriberFee = Decimal(row[30].value),
            DateAdded = to_datetime(row[31], datemode),
            DateUpdated = to_datetime(row[32], datemode),
            ShowSubscriberFee = bool(row[33].value),
            StartShowing = to_datetime(row[34], datemode),
            StopShowing = to_datetime(row[35], datemode),
        )

    def __repr__(self):
        return "Activity ActivityID={} ActivityTitle={}".format(self.ActivityID,
            self.ActivityTitle)
