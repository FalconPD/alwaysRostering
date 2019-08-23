import logging
import asyncio
import AR.AR as AR
import AR.schoology as schoology
import click
import pprint
import sys
import csv
from AR.tables import DistrictTeacher, Student

pp=pprint.PrettyPrinter()

@click.command()
@click.argument('db_file', type=click.Path(exists=True), metavar='DB_FILE')
@click.option('-e', '--environment', default='testing', show_default=True)
@click.option('-d', '--debug', is_flag=True, help="Print debugging statements")
@click.option('-f', '--force', is_flag=True, help="Perform possibly dangerous actions")
def main(db_file, environment, debug, force):
    """
    Syncs up Schoology users with a Genesis Database

    DB_FILE - A sqlite3 file of the Genesis database
    """
    loop = asyncio.get_event_loop()

    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    loop.run_until_complete(sync(loop, db_file, environment, force))
    loop.close()

async def create_task(tasks, loop, function):
    """
    Wrapper to make a task, start a task, and print status
    """

    tasks.append(
        loop.create_task(function)
    )
    await asyncio.sleep(0) # give the task a chance to start
    if len(tasks) % 500 == 0:
        print('{} tasks created'.format(len(tasks)))
    return tasks

def create_user_sets():
    """
    Creates sets of user IDs based on data in Genesis
    """
    print("Creating user sets from Genesis...")
    user_sets = {}

    user_sets['Student'] = { student.student_id for student in AR.students() }
    user_sets['Teacher'] = { teacher.teacher_id for teacher in AR.teachers() }
    user_sets['Administrator'] = { admin.teacher_id for admin in AR.admins() }
    user_sets['Sysadmin'] = { sysadmin.teacher_id for sysadmin in AR.sysadmins() }
    user_sets['EdServices'] = { teacher.teacher_id for teacher in AR.edservices() }
    staff = (user_sets['Teacher'] | user_sets['Administrator'] |
             user_sets['Sysadmin'] | user_sets['EdServices'])
    user_sets['All'] = user_sets['Student'] | staff

    # Users can only have one role. This keeps users in their highest
    # privileged role (sysadmin > admin > teacher > edservices)
    user_sets['EdServices'] -= (user_sets['Teacher'] | user_sets['Administrator']
                                | user_sets['Sysadmin'])
    user_sets['Teacher'] -= user_sets['Administrator'] | user_sets['Sysadmin']
    user_sets['Administrator'] -= user_sets['Sysadmin']

    # Make sure there is no overlap between staff and student IDs
    overlap = staff & user_sets['Student']
    if  len(overlap) > 0:
        logging.error("The following IDs show up in both staff and students: {}",
            ",".join(map(str, overlap)))
        sys.exit(1)

    for key, value in user_sets.items():
        print(f"    {key}: {len(value)}")

    return user_sets

async def get_users(loop, Schoology):
    """
    Creates a list of all users in Schoology
    """
    print("Getting a list of all users in Schoology...")
    users = []
    async with Schoology.Users as Users:
        retrieved = 0
        async for page in Users.list():
            users += page
            retrieved += len(page)
            if retrieved % 500 == 0:
                print(f"    {retrieved} users retrieved")
    return users

async def sync(loop, db_file, environment, force):
    """
    Performs all steps to sync Schoology user accounts
    """
    AR.init(db_file)
    user_sets = create_user_sets()
    async with schoology.Session(environment) as Schoology:
        async with Schoology.Users as Users:
            # Make a dict of genesis_ids -> schoology_uid
            results = await Users.csvexport(['school_uid', 'uid'])
            schoology_users = {}
            for row in csv.reader(results.splitlines()[1:]):
                schoology_users[str(row[0])] = str(row[1])

            # Check for accounts that need to be deleted
            deletes = set(schoology_users.keys()) - user_sets['All']
            len_deletes = len(deletes)
            print(f"Deleting {len_deletes} users...")

            # We have to update EVERYONE because we can't check a student's
            # advisors via the API
            print(f"Adding / Updating {len(user_sets['All'])}...")

            # Sanity checks
            if len_deletes > 25 and not force:
                logging.error(f"Attempting to delete {len_deletes} users, use "
                            "--force if you actually want to perform this action.")
                sys.exit(1)

            tasks=[]

            # Perform deletes
            for genesis_id in deletes:
                tasks = await create_task(tasks, loop,
                    Users.delete(schoology_users[genesis_id]))

            # Perform adds / updates
            for role, ids in user_sets.items():
                if role == 'Student':
                    for genesis_id in ids:
                        student = AR.student_by_id(genesis_id)
                        advisor_uids = ''
                        if student.counselor_id != '':
                            if student.counselor_id not in schoology_users:
                                logging.warning(f"Counselor "
                                                f"{student.counselor_id} for "
                                                f"{student} not found in "
                                                "Schoology.")
                            else:
                                advisor_uids = schoology_users[student.counselor_id]
                        tasks = await create_task(tasks, loop,
                            Users.add_update(
                                school_uid=student.student_id,
                                name_first=student.first_name,
                                name_last=student.last_name,
                                email=student.email,
                                role=role,
                                advisor_uids=advisor_uids,
                            )
                        )
                elif role != 'All':
                    for genesis_id in ids:
                        teacher = AR.teacher_by_id(genesis_id)
                        tasks = await create_task(tasks, loop,
                            Users.add_update(
                                school_uid=teacher.teacher_id,
                                name_first=teacher.first_name,
                                name_last=teacher.last_name,
                                email=teacher.email,
                                role=role
                            )
                        )
            await asyncio.gather(*tasks)

if __name__ == '__main__':
    main()
