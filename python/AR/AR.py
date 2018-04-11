import logging
from AR.tables import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json

def init(db_file):
    logging.debug('Loading database file {}'.format(db_file))
    engine = create_engine('sqlite:///{}'.format(db_file), echo=False)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()
