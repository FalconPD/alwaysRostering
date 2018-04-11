"""Allows automated interactions with the Genesis Student Information System.
"""
import logging
from urllib.parse import urlparse, parse_qs
import asyncio
import aiohttp
import json
from AR.tables import Base, sa_classes
import csv
import io
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

baseURL = 'https://genesis.monroe.k12.nj.us/'
credentials = json.load(open('../include/credentials.json'))

async def fetch_db(db_file, loop):
    """Perform all steps necessary to build a database while updating status.
    """
    engine = create_engine('sqlite:///{}'.format(db_file))
    DBSession = sessionmaker(bind=engine)
    db_session = DBSession()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    async with aiohttp.ClientSession(loop=loop) as session:
        print('Logging in to Genesis')
        await login(session=session)
        print('Getting tables: {}'.format(", ".join([cls.__tablename__ for cls in sa_classes])))
        await asyncio.gather(*[get_table(session, cls, db_session) for cls in sa_classes])
        db_session.commit()

async def get_table(session, cls, db_session):
    """Runs a report, downloads the output, and imports it into the database.
    """
    print('{}: running report'.format(cls.__tablename__))
    run_code = await start_report(session, cls)
    status = ''
    while status != 'COMPLETE':
        status = await get_status(session, run_code)
        await asyncio.sleep(1)
    print('{}: downloading report'.format(cls.__tablename__))
    text = await download(session, run_code)
    print('{}: importing into database'.format(cls.__tablename__))
    with io.StringIO(text, newline='') as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == cls.csv_header
        for row in reader:
            db_session.add(cls.from_csv(row))

async def login(session):
    """Login and get session cookie.

    Uses the username and password from credentials.json.
    """
    username = credentials['genesis']['username']
    password = credentials['genesis']['password']
    url = baseURL + 'genesis/sis/view'
    postURL = baseURL + 'genesis/sis/j_security_check'
    data = {
        'j_username': username,
        'j_password': password
    }
    logging.debug("Getting session cookie.")
    async with session.get(url) as resp:
        assert resp.status == 200
    logging.debug(resp.cookies)
    logging.debug("Logging in as {}".format(username))
    async with session.post(postURL, data=data) as resp:
        assert resp.status == 200

async def start_report(session, cls):
    """Sends a post request to start generating a report immediately.
    """
    url = baseURL + 'genesis/sis/view'
    params = {
        'module': 'reportWriter',
        'category': 'reports',
        'tab1': 'scheduleReport',
        'action': 'performQueueReport'
    }    
    data = {
        'fldReportCode': cls.report_code,
        'rwFormat': 'CSV',
        'fldSchedulingOption': 'NOW',
        'fldRunAtData': '',
        'fldHour': '',
        'fldMinute': '',
        'fldAMPM': '',
        'fldSchedYear': '*',
        'fldSchedMonth': '*',
        'fldSchedDay': '*',
        'fldSchedHour': '*',
        'fldSchedMinute': '*',
        'paramSSORT_SET_CODE': 'DEF',
        'paramSMAKESTUDENTLIST': '',
        'fldEmailUser': ''
    }
    async with session.post(url, params=params, data=data, allow_redirects=False) as resp:
        assert resp.status == 302
    location = resp.headers['Location']
    parseResult = urlparse(location)
    params = parse_qs(parseResult.query)
    return params['runcode'][0]

async def download(session, run_code):
  """Downloads the text of our report
  """
  url = baseURL + 'genesis/sis/view'
  params = {
    'module': 'reportWriter',
    'category': 'reports',
    'tab1': 'viewReport',
    'runcode': run_code,
    'action': 'rawopen'
  }
  async with session.get(url, params=params) as resp:
    return await resp.text()
      
async def get_status(session, run_code):
  """Updates the status object with the results of an AJAX query.
  """
  url = baseURL + 'genesis/sis/view'
  params = {
    'module': 'studentdata',
    'category': 'reports',
    'tab1': 'viewReport',
    'runcode': run_code,
    'action': 'ajaxGetQueuedReportStatus'
  }
  async with session.get(url, params=params) as resp:
    assert resp.status == 200
    responseJSON = await resp.json()
  logging.debug('get_status response: {}'.format(responseJSON))
  return responseJSON['status']
