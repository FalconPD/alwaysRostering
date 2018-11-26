import click
import asyncio
import logging
from sqlalchemy import func
import sys
import copy

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
    # If they are already in PG use their existing info as a basis for
    # updates
    payroll_id = teacher.other_id_number
    if payroll_id in PG.users:
        user = copy.deepcopy(PG.users[payroll_id])
    else:
        user = User()
        user.pg_id = None
        user.email = teacher.email
        user.payroll_id = payroll_id

    user.active = active

    # These are the only attributes we automatically update
    user.first_name=teacher.teacher_first_name
    user.last_name=teacher.teacher_last_name

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
            logging.warning("Missing payroll_id for {}".format(user))
        else:
            current_users[payroll_id]=create_user(teacher, True)

    for payroll_id, user in current_users.items():
        if user.pg_id == None:
            print("Adding: {}".format(user))
        else:
            if PG.users[payroll_id] != user:
                print("Updating: {}".format(user))
#                await PG.save_user(user)

#    in_pg = { user.pg_id for user in PG.users if user.active }
#    in_current_users = { user.pg_id for user in current_users }
#    deletes = in_pg - in_current_users
#    adds = in_current_users - in_pg
#    print("{} total deletes".format(len(deletes)))
#    for pg_id in deletes:
#        print("Deleting: {}".format(PG.user_by_id(pg_id)))

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
