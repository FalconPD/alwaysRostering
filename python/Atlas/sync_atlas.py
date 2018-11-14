import click
import asyncio
import logging
from sqlalchemy import func

import sys
sys.path.append('..')
import AR.AR as AR
import AR.atlas as atlas
from AR.tables import DistrictTeacher
from AR.atlas.user import User

async def sync_users():
    """
    Makes sure Genesis users and Atlas users are in sync    
    """
    current_users = {}

    # Create a dict of everyone who should be in Atlas and their attributes.
    # Add users that aren't in there yet.
    tasks = []
    for teacher in (
        AR.teachers()
        .union(AR.admins())
        .union(AR.edservices())
        .union(AR.curradmins())
        .union(AR.sysadmins())
    ):
        atlas_id = Atlas.id_map.get_atlas(teacher.teacher_id)
        user = User(atlas_id, teacher.teacher_first_name,
            teacher.teacher_last_name, teacher.email, [], [])
        if atlas_id == '': # If the user doesn't exist yet, create them
            print("Adding: {} {} (Genesis ID {})".format(
                teacher.teacher_first_name, teacher.teacher_last_name,
                teacher.teacher_id))
            tasks.append(Atlas.update_user(user, teacher.teacher_id))
        else:
            current_users[atlas_id] = user

    # We need the atlas_id to continue so we have to wait for the created users
    # and add them to our current_users
    for atlas_id in await asyncio.gather(*tasks):
        current_users[atlas_id] = Atlas.users[atlas_id]

    # Set attributes and privileges
    for teacher in AR.sysadmins():
        atlas_id = Atlas.id_map.get_atlas(teacher.teacher_id)
        user = current_users[atlas_id]
        user.attributes.append('System Admin')
    for teacher in AR.curradmins():
        atlas_id = Atlas.id_map.get_atlas(teacher.teacher_id)
        user = current_users[atlas_id]
        user.privileges.append('All-level editing privileges')
        
    # Check for differences between current_users and what's in Atlas
    tasks = []
    for atlas_id, atlas_user in Atlas.users.items():
        # Delete users in Atlas but not in our list
        if atlas_id not in current_users:
            print("Deleting: {} {} (Atlas ID {})".format(atlas_user.first_name,
                atlas_user.last_name, atlas_user.atlas_id))
            tasks.append(Atlas.delete_user(atlas_user))
            continue

        # Update users that are different
        genesis_id = Atlas.id_map.get_genesis(atlas_id)
        user = current_users[atlas_id]
        if not user.equal(atlas_user):
            print("Updating: {} {} {} (Atlas ID {})".format(user.first_name,
                user.last_name, user.email, user.atlas_id))
            tasks.append(Atlas.update_user(user, genesis_id))
            if len(tasks) > 100: # testing, one hundred at a time
                break;
            continue

    await asyncio.gather(*tasks)

    return
        
def create_map():
    """
    Perform a CASE INSENSITIVE search based on first_name and last_name for all
    users in Atlas to see if they are in Genesis. Creates a NEW id_map based on
    this information.
    """
    for atlas_id, user in Atlas.users.items():
        first = user.first_name
        last = user.last_name
        teacher = (AR.staff()
            .filter(func.upper(DistrictTeacher.teacher_first_name) == first.upper())
            .filter(func.upper(DistrictTeacher.teacher_last_name) == last.upper())
            .one_or_none()
        )
        if teacher == None:
            print("NOT FOUND {} {}".format(first, last))
        else:
            logging.debug("Atlas: {} {} {} -> Genesis: {} {} {}".format(
                atlas_id, first, last, teacher.teacher_id,
                teacher.teacher_first_name, teacher.teacher_last_name))
            Atlas.id_map.add(teacher.teacher_id, atlas_id)

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
    FORMAT = "[%(levelname)s %(filename)s:%(lineno)s - %(funcName)s()] %(message)s"
    if debug:
        logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    else:
        logging.basicConfig(level=logging.WARNING, format=FORMAT)

    # Setup a new event loop
    loop = asyncio.get_event_loop()

    # Load the Genesis database
    AR.init(db_file)

    # Create a new Atlas session (designed for an async with)
    Atlas = loop.run_until_complete(atlas.Session().__aenter__(map_file))
        
@cli.command(name="create_map")
def cli_create_map():
    """
    create id map based on first and last names 
    """
    create_map()

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
