import click
import asyncio
import logging
from sqlalchemy import func
import sys
import copy
import time

sys.path.append('..')
import AR.AR as AR
import AR.PG as professional_growth
from AR.PG.user import User

# This prevents some deepcopy errors
sys.setrecursionlimit(10000)

def create_user(teacher, active):
    """
    Atttempts to lookup a user on PG by their payroll ID, makes a copy of that
    user object, and updates certain attributes. New users are created.
    """
    payroll_id = teacher.other_id_number
    if payroll_id in PG.users:
        user = copy.deepcopy(PG.users[payroll_id])

        # These are the only attributes we automatically update
        user.first_name=teacher.teacher_first_name
        user.last_name=teacher.teacher_last_name
    else:
        user = User(teacher=teacher)

    return user

async def sync_users():
    """
    Makes sure Genesis users and Professional Growth users are in sync    
    """
    # Create a list of active users that should be setup in PG
    current_users = {}
    for teacher in (
        AR.cert_staff()                 # Certificated Staff
        .union(AR.secretaries())        # Secretaries
        .union(AR.sysadmins())          # IT
        .union(AR.hr_department())      # HR
        .union(AR.fieldtrip_admins())   # Everyone needed to approve a field trip
        .union(AR.media_staff())):      # Media staff are NOT all certificated
        payroll_id = teacher.other_id_number
        if payroll_id == '':
            logging.warning("Missing payroll_id for {}".format(teacher))
        else:
            current_users[payroll_id]=create_user(teacher, True)

    for payroll_id, user in current_users.items():
        if user.pg_id == None:
            print("Adding: {}".format(user))
#            await PG.save_user(user)
        else:
            if PG.users[payroll_id] != user:
                print("Updating: {}".format(user))
#                await PG.save_user(user)

    for payroll_id, user in PG.users.items():
        if payroll_id not in current_users:
            print("Deactivating: {}".format(user))

@click.group(chain=True)
@click.argument('genesis_db_file', type=click.Path(exists=True), metavar='GENESIS_DB')
@click.argument('pg_db_file', type=click.Path(writable=True), metavar='PG_DB')
@click.option("--debug", is_flag=True, help="Print debugging statements.")
def cli(genesis_db_file, pg_db_file, debug):
    """
    Command line interface for working with Frontline Professional Growth

    Loads the Genesis database from GENESIS_DB, uses the Professional Growth
    database located at PG_DB and performs COMMAND(s).
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
    AR.init(genesis_db_file)

    # Create a new PG session (designed for an async with)
    print("Logging into Professional Growth...")
    PG = loop.run_until_complete(
        professional_growth.Session(pg_db_file).__aenter__()
    )
        
@cli.command(name="sync_users")
def cli_sync_users():
    """
    sync up user accounts
    """
    loop.run_until_complete(sync_users())

@cli.command(name="download")
def cli_download():
    """
    downloads all tables from PG 
    """
    print("Downloading tables from Professional Growth...")
    loop.run_until_complete(PG.download())

@cli.resultcallback()
def cli_close(result, **kwargs):
    # Close down the PG session (designed for an async with)
    loop.run_until_complete(PG.__aexit__())
    loop.close()
    
if __name__ == '__main__':
    cli()
