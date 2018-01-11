import json
import logging
import argparse
import asyncio
import Genesis

async def print_status():
  done = False 
  while not done:
    done = True
    for report in Genesis.reports:
      if report['status'] != 'DONE':
        done = False
      print("{0[status]} {0[filename]} {0[percent]}% {0[message]}".format(report))
    await asyncio.sleep(2)

parser = argparse.ArgumentParser(description='Get the scripts used by alwaysRostering from Genesis')
parser.add_argument('-d', '--debug',
  help='print debugging statements',
  action='store_const',
  dest='loglevel',
  const=logging.DEBUG,
  default=logging.WARNING)
args = parser.parse_args()

logging.basicConfig(level=args.loglevel)

Genesis.queueReport(reportcode="991007", filename="rosters/classes.csv")
Genesis.queueReport(reportcode="990990", filename="rosters/students.csv")
Genesis.queueReport(reportcode="990989", filename="rosters/teachers.csv")
Genesis.queueReport(reportcode="991009", filename="rosters/schools.csv")

loop = asyncio.get_event_loop()
#loop.set_debug(True)
loop.run_until_complete(asyncio.gather(
  Genesis.run(),
  print_status()
))
loop.close()
