import click
import asyncio
import logging
from sqlalchemy import func

import sys
sys.path.append('..')
import AR.AR as AR
import AR.PG as professional_growth

async def sync_users():
    """
    Makes sure Genesis users and Professional Growth users are in sync    
    """
    await PG.save_user(PG.find_user("Ryan", "Tolboom"))

@click.group(chain=True)
@click.option("--debug", is_flag=True, help="Print debugging statements.")
@click.option("--user_file", type=click.Path(readable=True, writable=True),
    help="Load/Save the PG user database from/in this file. If it does not " +
    "exist it will be created with the data currently on PG.")
@click.argument('db_file', type=click.Path(exists=True), metavar='DB_FILE')
def cli(db_file, user_file, debug):
    """
    Command line interface for working with Frontline Professional Growth

    Loads the Genesis database from DB_FILE and performs COMMAND(s).
    """
    global loop
    global PG

    # Setup debugging
    FORMAT = "[%(levelname)s %(filename)s:%(lineno)s - %(funcName)s()] %(message)s"
    if debug:
        logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    else:
        logging.basicConfig(level=logging.WARNING, format=FORMAT)

    # Setup a new event loop
    loop = asyncio.get_event_loop()

    # Load the Genesis database
    print("Loading Genesis database...")
    AR.init(db_file)

    # Create a new PG session (designed for an async with)
    print("Logging into Professional Growth and loading users...")
    PG = loop.run_until_complete(professional_growth.Session(user_file).__aenter__())
        
@cli.command(name="sync_users")
def cli_sync_users():
    """
    sync up user accounts
    """
    loop.run_until_complete(sync_users())

@cli.resultcallback()
def cli_close(result, **kwargs):
    # Close down the PG session (designed for an async with)
    loop.run_until_complete(PG.__aexit__())
    loop.close()
    
if __name__ == '__main__':
    cli()
