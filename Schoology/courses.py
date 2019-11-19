"""
Syncs up Schoology courses
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
    print(f"Updating / Adding {total_courses} courses...")
    async with schoology.Session(environment) as Schoology:
        async with Schoology.Courses as Courses:
            tasks = []
            for course in AR.courses():
                building_code = course.school_code
                title = course.course_description
                course_code = course.school_code + ' ' + course.course_code
                sections = []
                for section in course.active_sections:
                    semesters = section.semesters
                    if 'FY' in semesters: # There is only ONE full year
                        grading_periods = [f"{section.school_year} FY"]
                    else: # Others are per building
                        grading_periods = []
                        for semester in semesters:
                            grading_periods.append(f"{section.school_year} "
                                                   f"{section.school_code} "
                                                   f"{semester}")
                    grading_period_ids = []
                    for grading_period in grading_periods:
                        grading_period_id = Schoology.GradingPeriods.lookup_id(
                                grading_period)
                        if grading_period_id == None:
                            logging.warning("Unable to lookup grading period "
                                            "id for "
                                            f"{section.section_school_code} "
                                            "(Are the grading periods synced "
                                            "with Schoology?)")
                        else:
                            grading_period_ids.append(grading_period_id)
                    if grading_period_ids != []:
                        sections.append({
                            'title': section.name,
                            'section_school_code': section.section_school_code,
                            'grading_periods': grading_period_ids,
                        })
                tasks.append(
                    Courses.add_update(building_code, title, course_code, sections)
                )
            await utils.task_monitor(tasks)

if __name__ == '__main__':
    main()
