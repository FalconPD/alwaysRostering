import sqlalchemy
from sqlalchemy import Column, Integer, String
from AR.PG.tables import Base

class ActivityObjective(Base):
    __tablename__ = 'Activities_Objectives'

    ActivityID      = Column(Integer)
    ActivityTitle   = Column(String)
    AObjectiveID    = Column(Integer, primary_key=True)
    ObjectiveTitle  = Column(String)
    ObjectiveDesc   = Column(String)

    @classmethod
    def from_row(cls, row, datemode):
        """
        Factory function for making a ActivityObjective from an xlrd row
        """
        return cls(
            ActivityID      = int(row[0].value),
            ActivityTitle   = row[1].value,
            AObjectiveID    = int(row[2].value),
            ObjectiveTitle  = row[3].value,
            ObjectiveDesc   = row[4].value,
        )

    def __repr__(self):
        return f("ActivityObjective "
            "AObjectiveID={self.AObjectiveID} "
            "ActivityID={self.ActivityID} "
            "ObjectiveTitle={self.ObjectiveTitle}"
        )
