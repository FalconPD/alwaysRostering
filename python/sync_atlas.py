import AR.AR as AR
import AR.atlas as atlas
import click
import asyncio
import logging
from AR.tables import DistrictTeacher
from sqlalchemy import func

@click.command()
@click.argument('db_file', type=click.Path(exists=True), metavar='DB_FILE')
@click.option("--debug", is_flag=True, help="Print debugging statements")
def main(db_file, debug):
    """
    Syncs up Rubicon Atlas with a Genesis Database

    DB_FILE - A sqlite3 file of the Genesis database
    """
    loop = asyncio.get_event_loop()

    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    loop.run_until_complete(sync(loop=loop, db_file=db_file))
    loop.close()

async def sync(loop, db_file):
    """
    Performs all steps to sync Atlas with a Genesis Database
    """
    AR.init(db_file)
    async with atlas.Session() as Atlas:
        await Atlas.Users.test()
        # Add teachers that aren't in Atlas
#        for teacher in AR.teachers():
#            first = teacher.teacher_first_name
#            last = teacher.teacher_last_name
#            email = teacher.email
#            result = Atlas.Users.find_by_name(first, last)
#            if result == None:
#                print("Adding teacher {}".format(teacher))
#                await Atlas.Users.add_user(first, last, email)
        # Delete users that aren't ACTIVE in Genesis
#        for user in Atlas.Users.users:
            # Perform a CASE INSENSITIVE search based on FIRST and LAST
#            # In the future this should be by their email address
#            first = user['First Name']
#            last = user['Last Name']
#            count = (AR.staff()
#                .filter(func.upper(DistrictTeacher.teacher_first_name) == first.upper())
#                .filter(func.upper(DistrictTeacher.teacher_last_name) == last.upper())
#                .count()
#            )
#            if count == 0:
#                print("{}, {}".format(first, last))
        

if __name__ == '__main__':
    main()
