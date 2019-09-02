# In our python environment
import logging
import asyncio
import click
import sys

# In the alwaysRostering environment
import AR.AR as AR
import AR.schoology as schoology

# Local
import utils

@click.command()
@click.argument('db_file', type=click.Path(exists=True), metavar='DB_FILE')
@click.option('-e', '--environment', default='testing', show_default=True)
@click.option('-d', '--debug', is_flag=True, help="Print debugging statements")
def main(db_file, environment, debug):
    """
    Adds Schoology enrollments based on sections in a Genesis Database

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
    Performs all steps to perform Schoology enrollments
    """
    print(f"Loading {db_file}...")
    AR.init(db_file)
    async with schoology.Session(environment) as Schoology:
        async with Schoology.Enrollments as Enrollments:
            len_sections = AR.sections().count()
            print(f"Enrolling students and teachers in {len_sections} sections...")
            tasks = []
            for section in AR.sections():
                # enroll the teacher
                section_school_code = section.section_school_code
                teacher_id = section.first_subsection.teacher_id
                tasks.append(
                    Enrollments.add(section_school_code, teacher_id, admin=True)
                )
            # enroll the students
                for student in section.active_students:
                    student_id = student.student_id
                    tasks.append(
                        Enrollments.add(section_school_code, student_id)
                    )
            await utils.task_monitor(tasks, 30)

if __name__ == '__main__':
    main()
