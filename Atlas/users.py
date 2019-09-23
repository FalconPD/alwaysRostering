# System
import click
import asyncio
import logging
from sqlalchemy import func
import sys

# alwaysRostering
import AR.AR as AR
import AR.atlas as atlas
from AR.tables import DistrictTeacher
from AR.atlas.user import User

async def sync(loop, db_file):
    """
    Syncs Atlas users with a Genesis DB file
    """
    AR.init(db_file)

    print("Creating user sets...")
    sysadmins = { teacher.teacher_id for teacher in (
        AR.sysadmins()
        .union(AR.hr_department())
        .union(AR.curriculum_secretaries())
    ) }
    curriculum_admins = { teacher.teacher_id for teacher in AR.curradmins() }
    all = sysadmins | curriculum_admins | { teacher.teacher_id for teacher in (
        AR.teachers()
        .union(AR.admins())
        .union(AR.edservices())
    ) }
    print(f"    Sysadmins: {len(sysadmins)}")
    print(f"    Curriculum Admins: {len(curriculum_admins)}")
    print(f"    Total: {len(all)}")

    async with atlas.Session() as Atlas:
        email_to_user = Atlas.email_to_user() # makes a mapping dict
        tasks = []
        expected_ids = set()
        for teacher_id in all:
            teacher = AR.teacher_by_id(teacher_id)
            first_name = teacher.first_name
            last_name = teacher.last_name
            former_name = teacher.former_name
            email = teacher.email
            atlas_user = None

            # Try to look a person up by email
            if email != None:
                upper_email = email.upper()
                if upper_email in email_to_user:
                    atlas_user = email_to_user[upper_email]

            # Otherwise use their first and last name
            if atlas_user == None:
                atlas_user = Atlas.find_user_by_name(first_name, last_name)

            # Finally try their maiden name
            if atlas_user == None:
                if former_name != '' and former_name != None:
                    atlas_user = Atlas.find_user_by_name(first_name, former_name)

            # If all else fails, create them
            if atlas_user == None:
                print(f"Adding: {teacher}")
                atlas_user = User('', first_name, last_name, [email], [], [])
                # we have to wait for this to get the atlas_id
                atlas_user = await Atlas.update_user(atlas_user)

            if atlas_user != None:
                if (atlas_user.first_name != first_name or
                    atlas_user.last_name != last_name or
                    email not in atlas_user.emails or
                    teacher_id in sysadmins and 'System Admin' not in atlas_user.attributes or
                    teacher_id in curriculum_admins and 'All-level editing privileges' not in atlas_user.privileges):
                    print(f"Updating: {teacher}")
                    atlas_user.first_name = first_name
                    atlas_user.last_name = last_name
                    atlas_user.emails = [email]
                    if teacher_id in sysadmins:
                        atlas_user.attributes.append('System Admin')
                    if teacher_id in curriculum_admins:
                        atlas_user.privileges.append('All-level editing privileges')
                    tasks.append(Atlas.update_user(atlas_user))
                expected_ids.add(atlas_user.atlas_id)

        for atlas_id in (Atlas.users.keys() - expected_ids):
            print(f"{Atlas.users[atlas_id]} not in the list of expected Atlas "
                  "users. Consider deleting manually.")

        await asyncio.gather(*tasks)

@click.command()
@click.option("--debug", is_flag=True, help="Print debugging statements")
@click.argument('db_file', type=click.Path(exists=True), metavar='DB_FILE')
def main(debug, db_file):
    """
    Syncs Atlas user accounts with Genesis database file DB_FILE
    """
    # Set up debugging
    FORMAT = "[%(levelname)s %(filename)s:%(lineno)s - %(funcName)s()] %(message)s"
    if debug:
        logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    else:
        logging.basicConfig(level=logging.WARNING, format=FORMAT)

    # Set up a new event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(sync(loop, db_file))

if __name__ == '__main__':
    main()
