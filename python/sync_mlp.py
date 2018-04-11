import logging
import argparse
import asyncio
import AR.mlp as mlp

parser = argparse.ArgumentParser(description='Sync MyLearningPlan user database with Genesis information')
parser.add_argument('-d', '--debug',
    help='print debugging statements',
    action='store_const',
    dest='loglevel',
    const=logging.DEBUG,
    default=logging.WARNING)
args = parser.parse_args()

logging.basicConfig(level=args.loglevel)

loop = asyncio.get_event_loop()
#loop.set_debug(True)
loop.run_until_complete(mlp.run(loop))
loop.close()
