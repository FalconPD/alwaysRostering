import logging
import argparse
import asyncio
from AR import Genesis

parser = argparse.ArgumentParser(description='Create database from the information in Genesis')
parser.add_argument('-d', '--debug',
    help='print debugging statements',
    action='store_const',
    dest='loglevel',
    const=logging.DEBUG,
    default=logging.WARNING)
parser.add_argument('db_file',
    help='file to save database to')

args = parser.parse_args()

logging.basicConfig(level=args.loglevel)

loop = asyncio.get_event_loop()
#loop.set_debug(True)
loop.run_until_complete(Genesis.fetch_db(args.db_file, loop))
loop.close()
