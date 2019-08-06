import sqlalchemy
from sqlalchemy import Column, Integer, String
from AR.PG.tables import Base

class Goal(Base):
    __tablename__ = 'Goals'

    GoalID         = Column(Integer, primary_key=True)
    UserID         = Column(Integer)
    DistrictID     = Column(Integer)
    GoalTitle      = Column(String)
    GoalDesc       = Column(String)
    ObjectiveID    = Column(Integer, primary_key=True)
    ObjectiveTitle = Column(String)
    ObjectiveDesc  = Column(String)

    @classmethod
    def from_row(cls, row, datemode):
        """
        Factory function for a Goal from the xlrd row
        """
        return cls(
            GoalID         = int(row[0].value),
            UserID         = int(row[1].value),
            DistrictID     = int(row[2].value),
            GoalTitle      = row[3].value,
            GoalDesc       = row[4].value,
            ObjectiveID    = int(row[5].value),
            ObjectiveTitle = row[6].value,
            ObjectiveDesc  = row[7].value,
        )

    def __repr__(self):
        return f("Goal "
            "GoalID={self.GoalID} "
            "GoalTitle={self.GoalTitle} "
            "ObjectiveID={self.ObjectiveID} "
            "ObjectiveTitle={self.ObjectiveTitle} "
        )
