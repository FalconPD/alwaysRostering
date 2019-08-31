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
def main(db_file, environment, debug):
    """
    Syncs up Schoology buildings with a Genesis Database

    DB_FILE - A sqlite3 file of the Genesis database
    """
    loop = asyncio.get_event_loop()

    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    loop.run_until_complete(sync(loop, db_file, environment))
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
        print(f"{len(tasks)} tasks created")
    return tasks

async def sync(loop, db_file, environment):
    """
    Performs all steps to sync Schoology buildings

    NOTE: Genesis uses the term 'schools' to refer to the individual
    buildings, Schoology uses buildings. In Schoology there is one school,
    'Monroe Township Schools' and currently 8 buildings (AES, BBS, BES, etc.)
    """
    AR.init(db_file)
    async with schoology.Session(environment) as Schoology:
        async with Schoology.Buildings as Buildings:
            tasks=[]
            for building in AR.schools():
                await create_task(tasks, loop,
                    Buildings.add_update(
                        title=building.school_name,
                        building_code=building.building_code,
                        address1=building.school_address1,
                        address2=building.school_address2,
                        phone=building.school_office_phone,
                        website=building.school_url
                    )
                )
            await asyncio.gather(*tasks)

if __name__ == '__main__':
    main()
