import click
import asyncio
import logging
from sqlalchemy import func

import sys
sys.path.append('..')
import AR.AR as AR
import AR.atlas as atlas
from AR.tables import DistrictTeacher

async def sync_users():
    """
    Goes through all users in Genesis
    """
#    teacher = AR.staff().filter(DistrictTeacher.teacher_id=='099').one()
#    await Atlas.Users.add_update(teacher.teacher_id, teacher.first_name, teacher.last_name,
#        teacher.email, admin=True)
    atlas_users = set()
    teachers = set()
    for user in Atlas.Users.users:
        genesis_id = Atlas.Users.atlas_to_genesis(user['atlas_id'])
        if genesis_id == None:
            print(user)
        else:
            atlas_users.add(genesis_id)
    for teacher in AR.teachers().union(AR.admins()).union(AR.edservices()).union(AR.sysadmins()):
        teachers.add(teacher.teacher_id)
    print(atlas_users - teachers)
    await Atlas.Users.delete_object('719')
    

def create_map(verbose):
    """
    Perform a CASE INSENSITIVE search based on first_name and last_name for all
    users in Atlas to see if they are in Genesis. Creates a NEW id_map based on
    this information.
    """
    id_map = []

    for user in Atlas.Users.users:
        first = user['first_name']
        last = user['last_name']
        atlas_id = user['atlas_id']
        teacher = (AR.staff()
            .filter(func.upper(DistrictTeacher.teacher_first_name) == first.upper())
            .filter(func.upper(DistrictTeacher.teacher_last_name) == last.upper())
            .one_or_none()
        )
        if teacher == None:
            print("NOT FOUND {} {}".format(first, last))
        else:
            if (verbose):
                print("Atlas: {} {} {} -> Genesis: {} {} {}".format(atlas_id, first, last,
                    teacher.teacher_id, teacher.teacher_first_name,
                    teacher.teacher_last_name))
            id_map.append({'atlas_id': atlas_id, 'genesis_id': teacher.teacher_id})
            Atlas.Users.id_map = id_map

@click.group(chain=True)
@click.option("--debug", is_flag=True, help="Print debugging statements")
@click.argument('db_file', type=click.Path(exists=True), metavar='DB_FILE')
@click.argument('map_file', type=click.Path(readable=True, writable=True),
    metavar='MAP_FILE')
def cli(db_file, map_file, debug):
    """
    Loads the Genesis database from DB_FILE and the Atlas to Genesis ID map
    from MAP_FILE before performing COMMAND(s).
    """
    global loop
    global Atlas

    # Setup debugging
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    # Setup a new event loop
    loop = asyncio.get_event_loop()

    # Load the Genesis database
    AR.init(db_file)

    # Create a new Atlas session (designed for an async with)
    Atlas = loop.run_until_complete(atlas.Session().__aenter__(map_file))
        
@cli.command(name="create_map")
@click.option("--verbose", is_flag=True, help="Print all matches") 
def cli_create_map(verbose):
    """
    create id map based on first and last names 
    """
    create_map(verbose)

@cli.command(name="sync_users")
def cli_sync_users():
    """
    sync up user accounts
    """
    loop.run_until_complete(sync_users())

@cli.resultcallback()
def cli_close(result, **kwargs):
    # Close down the Atlas session (designed for an async with)
    loop.run_until_complete(Atlas.__aexit__())
    loop.close()
    
if __name__ == '__main__':
    cli()
