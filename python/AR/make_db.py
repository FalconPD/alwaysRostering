import json
import logging
import argparse
import asyncio
import Genesis
import time

async def update_status():
  while True:
    for status in Genesis.statuses:
      print('{0[name]}: {0[status]} {0[percent]}% {0[message]}'.format(status))
    await asyncio.sleep(2)

async def run(update_task, filename):
  await Genesis.make_db(filename)
  update_task.cancel()

parser = argparse.ArgumentParser(description='Build a database from Genesis reports')
parser.add_argument('-d', '--debug',
  help='print debugging statements',
  action='store_const',
  dest='loglevel',
  const=logging.DEBUG,
  default=logging.WARNING)
args = parser.parse_args()

logging.basicConfig(level=args.loglevel)

filename = 'db/genesis-{}.sqlite3'.format(int(time.time()))

loop = asyncio.get_event_loop()
#loop.set_debug(True)
update_task = loop.create_task(update_status())
loop.run_until_complete(run(update_task, filename))
loop.close()
