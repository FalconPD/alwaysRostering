import sqlalchemy
from sqlalchemy import Column, Integer, String, Boolean
from AR.PG.tables import Base

class ActivityFormat(Base):
    __tablename__ = 'ActivityFormats'

    ActivityFormatID    = Column(Integer, primary_key=True)
    DistrictID          = Column(Integer)
    ActivityFormatDesc  = Column(String)
    Order               = Column(Integer)
    ShortName           = Column(String)
    Active              = Column(Boolean)
    Code                = Column(String)
    Bankable            = Column(Boolean)

    @classmethod
    def from_row(cls, row, datemode):
        """
        Factory function for a Activity from the xlrd row
        """
        return cls(
            ActivityFormatID    = int(row[0].value),
            DistrictID          = int(row[1].value),
            ActivityFormatDesc  = row[2].value,
            Order               = int(row[3].value),
            ShortName           = row[4].value,
            Active              = bool(row[5].value),
            Code                = row[6].value,
            Bankable            = bool(row[7].value),
        )

    def __repr__(self):
        return "ActivityFormat ActivityFormatID={} ShortName={}".format(
            self.ActivityFormatID, self.ShortName)
