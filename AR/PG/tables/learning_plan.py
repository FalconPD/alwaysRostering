import sqlalchemy
from sqlalchemy import Column, Integer, String, Boolean, Date, Float
from AR.PG.tables import Base
from AR.PG.tables.utils import to_datetime
 
class LearningPlan(Base):
    __tablename__ = 'LearningPlan'

    LearningPlanID      = Column(Integer, primary_key=True)
    DistrictID          = Column(Integer)
    ActivityID          = Column(Integer)
    UserID              = Column(Integer)
    PaymentFormatID     = Column(Integer)
    CCatalogID          = Column(Integer)
    EventID             = Column(Integer)
    Type                = Column(String)
    SubmissionDate      = Column(Date)
    StartDate           = Column(Date)
    ActivityTitle       = Column(String)
    ActivityDesc        = Column(String)
    URL                 = Column(String)
    ActivityHours       = Column(Float)
    Credits             = Column(Float)
    ApprovalRequired    = Column(Boolean)
    ApprovalStatus      = Column(Integer)
    Reapproval          = Column(Boolean)
    DateExpired         = Column(Date)
    HoursAttended       = Column(Float)
    InstructorUserID    = Column(Integer)
    InstructorName      = Column(String)
    DateCompleted       = Column(Date)
    MeetingDates        = Column(String)
    FormID              = Column(Integer)
    ActivityFormatID    = Column(Integer)
    CourseSubjectArea   = Column(String)
    ProviderID          = Column(Integer)
    ProviderName        = Column(String)
    EndDate             = Column(Date)
    SubRequried         = Column(Boolean)
    SubRequested        = Column(String)
    Comments            = Column(String)
    PDEReference        = Column(Integer)
    PDEResubmit         = Column(Boolean)
    ConferenceLocation  = Column(String)
    SolutionWhereID     = Column(String)
    EmailTeacher        = Column(Boolean)
    MaxUsers            = Column(Integer)
    CourseCode          = Column(String)
    IsActivityProposal  = Column(Boolean)

    @classmethod
    def from_row(cls, row, datemode):
        """
        Factory function for a LearningPlan from the xlrd row
        """
        return cls(
            LearningPlanID      = int(row[0].value),
            DistrictID          = int(row[1].value),
            ActivityID          = int(row[2].value),
            UserID              = int(row[3].value),
            PaymentFormatID     = int(row[4].value),
            CCatalogID          = int(row[5].value),
            EventID             = int(row[6].value),
            Type                = row[7].value,
            SubmissionDate      = to_datetime(row[8], datemode),
            StartDate           = to_datetime(row[9], datemode),
            ActivityTitle       = row[10].value,
            ActivityDesc        = row[11].value,
            URL                 = row[12].value,
            ActivityHours       = float(row[13].value),
            Credits             = float(row[14].value),
            ApprovalRequired    = bool(row[15].value),
            ApprovalStatus      = int(row[16].value),
            Reapproval          = bool(row[17].value),
            DateExpired         = to_datetime(row[18], datemode),
            HoursAttended       = float(row[19].value),
            InstructorUserID    = int(row[20].value),
            InstructorName      = row[21].value,
            DateCompleted       = to_datetime(row[22], datemode),
            MeetingDates        = row[23].value,
            FormID              = int(row[24].value),
            ActivityFormatID    = int(row[25].value),
            CourseSubjectArea   = row[26].value,
            ProviderID          = int(row[27].value),
            ProviderName        = row[28].value,
            EndDate             = to_datetime(row[29], datemode),
            SubRequried         = bool(row[30].value),
            SubRequested        = row[31].value,
            Comments            = row[32].value,
            PDEReference        = int(row[33].value),
            PDEResubmit         = bool(row[34].value),
            ConferenceLocation  = row[35].value,
            SolutionWhereID     = row[36].value,
            EmailTeacher        = bool(row[37].value),
            MaxUsers            = int(row[38].value),
            CourseCode          = row[39].value,
            IsActivityProposal  = bool(row[40].value),
        )

    def __repr__(self):
        return "LearningPlan LearningPlanID={} ActivityID={} UserID={} ActivityTitle={}".format(
            self.LearningPlanID, self.ActivityID, self.UserID, self.ActivityTitle)
