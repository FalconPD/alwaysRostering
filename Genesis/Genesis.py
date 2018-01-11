"""Allows automated interactions with the Genesis Student Information System.
"""
import logging
from urllib.parse import urlparse, parse_qs
import asyncio
import aiohttp
import json

baseURL = 'https://genesis.monroe.k12.nj.us/'
credentials = json.load(open('../include/credentials.json'))
reports = []

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

async def start_report(session, report):
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
    'fldReportCode': report['report_code'],
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
  report['run_code'] = params['runcode'][0]
  report['status'] = 'STARTED'

async def download(session, report):
  """Downloads a report asynchronously, updating status as it does
  """
  url = baseURL + 'genesis/sis/view'
  params = {
    'module': 'reportWriter',
    'category': 'reports',
    'tab1': 'viewReport',
    'runcode': report['run_code'],
    'action': 'rawopen'
  }
  report['status'] = 'DOWNLOADING'
  report['message'] = 'Downloading...'
  with open(report['filename'], 'wb') as fh:
    async with session.get(url, params=params) as resp:
      total_bytes = int(resp.headers['content-length'])
      async for chunk in resp.content.iter_any():
        report['percent'] = str(int(len(chunk)*100/total_bytes))
        fh.write(chunk)
  report['status'] = 'DONE'

async def update_report(session, report):
  """Updates the report object with the results of an AJAX query.
  """
  url = baseURL + 'genesis/sis/view'
  params = {
    'module': 'studentdata',
    'category': 'reports',
    'tab1': 'viewReport',
    'runcode': report['run_code'],
    'action': 'ajaxGetQueuedReportStatus'
  }
  async with session.get(url, params=params) as resp:
    assert resp.status == 200
    responseJSON = await resp.json()
  report['status'] = responseJSON['status']
  report['percent'] = responseJSON['percent']
  report['message'] = responseJSON['engineMessage']

async def get_report(session, report):
  """Performs the entire report process while updating status.
  """
  await start_report(session, report)
  while report['status'] != 'COMPLETE':
    await update_report(session, report)
    await asyncio.sleep(1)
  await download(session, report)
  report['percent'] = 100
  report['message'] = ''
  
async def run():
  """Logs in and gets all the queued reports.
  """
  async with aiohttp.ClientSession() as session:
    await login(session)
    coros = []
    for report in reports:
      coros.append(get_report(session, report))
    await asyncio.gather(*coros)
  del reports[:]

def queueReport(reportcode, filename):
  """Add a report to the list of reports that will be fetched.
  """
  reports.append({'report_code': reportcode, 'filename': filename, 'run_code': '',
    'status': 'NOT STARTED', 'percent': '0', 'message': ''})
