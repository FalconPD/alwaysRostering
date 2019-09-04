"""
Used one-time to roll created courses back to the previous year's grading period
"""

# System
import logging
import asyncio
import click
import sys

# alwaysRostering
import AR.AR as AR
import AR.schoology as schoology

# Schoology scripts
sys.path.append("..")
import utils

@click.command()
@click.argument('db_file', type=click.Path(exists=True), metavar='DB_FILE')
@click.option('-e', '--environment', default='testing', show_default=True)
@click.option('-d', '--debug', is_flag=True, help="Print debugging statements")
def main(db_file, environment, debug):
    """
    Syncs up Schoology courses with a Genesis Database

    DB_FILE - A sqlite3 file of the Genesis database
    """
    loop = asyncio.get_event_loop()

    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    loop.run_until_complete(sync(loop, db_file, environment))
    loop.close()

async def sync(loop, db_file, environment):
    """
    Performs all steps to sync Schoology courses
    """
    print(f"Loading {db_file}...")
    AR.init(db_file)
    total_courses = AR.courses().count()
    print(f"Rolling back grading period on {total_courses} courses...")
    async with schoology.Session(environment) as Schoology:
        async with Schoology.Courses as Courses:
            tasks = []
            for course in AR.courses():
                building_code = course.school_code
                title = course.course_description
                course_code = course.school_code + ' ' + course.course_code
                sections = []
                for section in course.active_sections:
                    semester = section.semester
                    grading_period_id = Schoology.GradingPeriods.lookup_id("All Year 2018-2019")
                    if grading_period_id == None:
                        logging.warning("Unable to lookup grading period id for "
                                        f"{section.section_school_code} (Are "
                                        "the grading periods synced with "
                                        "Schoology?)")
                    else:
                        sections.append({
                            'title': section.name,
                            'section_school_code': section.section_school_code,
                            'grading_periods': grading_period_id,
                        })
                tasks.append(
                    Courses.add_update(building_code, title, course_code, sections)
                )
            await utils.task_monitor(tasks)

if __name__ == '__main__':
    main()
