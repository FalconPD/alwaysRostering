"""Allows automated interactions with the Genesis Student Information System.
"""
import logging
from urllib.parse import urlparse, parse_qs
import asyncio
import aiohttp
import json
from tables import TABLES
import sqlite3
import csv

baseURL = 'https://genesis.monroe.k12.nj.us/'
credentials = json.load(open('../../include/credentials.json'))
statuses = []

async def make_db(file_name):
  """Perform all steps necessary to build a database while updating status.
  """
  conn = sqlite3.connect(file_name)
  db_cursor = conn.cursor()
  async with aiohttp.ClientSession() as session:
    await login(session)
    coros = []
    del statuses[:]
    for TABLE in TABLES:
      logging.debug('Creating table {0[name]} and queing report_code {0[report_code]}'.format(TABLE))
      db_cursor.execute(TABLE['sql_schema'])
      status = {'name': TABLE['name'], 'status': 'NOT STARTED', 'percent': '0', 'message': ''}
      statuses.append(status)
      coros.append(get_table(db_cursor, session, TABLE, status))
    await asyncio.gather(*coros)
  conn.commit()
  conn.close()

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

async def start_report(session, TABLE, status):
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
    'fldReportCode': TABLE['report_code'],
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
  status['run_code'] = params['runcode'][0]
  status['status'] = 'STARTED'

async def download(db_cursor, session, TABLE, status):
  """Downloads / Imports a table asynchronously, updating status as it does
  """
  url = baseURL + 'genesis/sis/view'
  params = {
    'module': 'reportWriter',
    'category': 'reports',
    'tab1': 'viewReport',
    'runcode': status['run_code'],
    'action': 'rawopen'
  }
  status['status'] = 'DOWNLOADING/IMPORTING'
  status['message'] = 'Downloading data and importing into database'
  async with session.get(url, params=params) as resp:
    total_bytes = int(resp.headers['content-length'])
    downloaded = 0
    header = await resp.content.readline()
    csv_header = next(csv.reader([header.decode("utf-8")]))
    assert TABLE['csv_header'] == csv_header    
    async for line in resp.content:
      downloaded += len(line)
      status['percent'] = str(int(downloaded*100/total_bytes))
      row = next(csv.reader([line.decode("utf-8")]))
      assert TABLE['columns'] == len(row)
      db_cursor.execute(TABLE['sql_insert'], row)
      
async def update_report(session, status):
  """Updates the status object with the results of an AJAX query.
  """
  print("Updating status")
  url = baseURL + 'genesis/sis/view'
  params = {
    'module': 'studentdata',
    'category': 'reports',
    'tab1': 'viewReport',
    'runcode': status['run_code'],
    'action': 'ajaxGetQueuedReportStatus'
  }
  async with session.get(url, params=params) as resp:
    assert resp.status == 200
    responseJSON = await resp.json()
  status['status'] = responseJSON['status']
  status['percent'] = responseJSON['percent']
  status['message'] = responseJSON['engineMessage']

async def get_table(db_cursor, session, TABLE, status):
  """Perform the entire table retrieving process while updating status.
  """
  await start_report(session, TABLE, status)
  while status['status'] != 'COMPLETE':
    await update_report(session, status)
    await asyncio.sleep(1)
  await download(db_cursor, session, TABLE, status)
  status['percent'] = 100
  status['message'] = ''
  status['status'] = 'DONE'
