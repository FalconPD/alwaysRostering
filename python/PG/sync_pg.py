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

def create_user(teacher):
    """
    Atttempts to lookup a user on PG by their payroll ID or first and last
    name, makes a copy of that user object, and updates certain attributes. New
    users are created.
    """
    # If they are already in PG use their existing info as a basis for
    # updates
    user = PG.user_by_payroll(teacher.other_id_number)
    if user == None:
        user = PG.user_by_name(teacher.teacher_first_name,
            teacher.teacher_last_name)
    if user != None:
        new_user = copy.deepcopy(user)
    else:
        print("Adding: {}".format(teacher))
        new_user = User()
        new_user.pg_id = None
        new_user.active = True

    # These are the only attributes we automatically update
    new_user.first_name=teacher.teacher_first_name
    new_user.last_name=teacher.teacher_last_name
    new_user.payroll_id=teacher.other_id_number

    return new_user

async def sync_users():
    """
    Makes sure Genesis users and Professional Growth users are in sync    
    """
    # Create a list of active users that should be setup in PG
    current_users = []
    for teacher in AR.teachers():
        current_users.append(create_user(teacher))
    for admin in AR.admins():
        current_users.append(create_user(admin))
    for edservice in AR.edservices():
        current_users.append(create_user(edservice))
    for fieldtrip_admin in AR.fieldtrip_admins():
        current_users.append(create_user(fieldtrip_admin))
    for sysadmin in AR.sysadmins():
        current_users.append(create_user(sysadmin))

    in_pg = { user.pg_id for user in PG.users if user.active }
    in_current_users = { user.pg_id for user in current_users }
    for pg_id in in_pg - in_current_users:
        print("Deleting: {}".format(PG.user_by_id(pg_id)))

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
