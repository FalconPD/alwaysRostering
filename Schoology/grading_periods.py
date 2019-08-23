from AR.tables import SchoolAttendanceCycle
import AR.AR as AR
import click
import AR.schoology as schoology
import asyncio
import logging
import re
import sys
import pprint
import datetime

pp = pprint.PrettyPrinter()

@click.command()
@click.option('-e', '--environment', default='testing', show_default=True)
@click.option('-d', '--debug', is_flag=True)
@click.argument('db_file', type=click.Path(exists=True), metavar='DB_FILE')
@click.argument('school_year', metavar='SCHOOL_YEAR')
def main(environment, debug, db_file, school_year):
    """
    Syncs Schoology grading periods with Genesis semesters. Currently syncs FY
    for the whole district and S1, S2, Q1, Q2, Q3, Q4 for each building. Uses
    dates from a previous year if the current year cannot be found.

    \b
    DB_FILE - A sqlite3 file of the Genesis database
    SCHOOL_YEAR - School year to sync, ex. 2018-19
    """
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)


    # Initialize alwaysRostering
    AR.init(db_file)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(sync(environment, school_year))
    loop.close()

def attendance_cycle(code, school_code, school_year):
    """
    Looks up an attendance cycle and returns the previous year's dates (day and
    month) if it isn't found. Errors out if the previous year's can't be found.
    """
    # Derive the previous school year in case we need it
    matches = re.match('(\d+)-(\d+)', school_year)
    start = int(matches.group(1)) - 1
    end = int(matches.group(2)) - 1
    prev_school_year = f"{start}-{end}"

    cycle = (
        AR.db_session.query(SchoolAttendanceCycle)
        .filter(SchoolAttendanceCycle.code==code)
        .filter(SchoolAttendanceCycle.school_year==school_year)
        .filter(SchoolAttendanceCycle.school_code=='MTHS')
        .one_or_none()
    )
    if cycle == None:
        logging.warning(f"{code} for {school_year} not found, using "
            f"{prev_school_year}")
        prev_cycle = (
            AR.db_session.query(SchoolAttendanceCycle)
            .filter(SchoolAttendanceCycle.code==code)
            .filter(SchoolAttendanceCycle.school_year==prev_school_year)
            .filter(SchoolAttendanceCycle.school_code=='MTHS')
            .one_or_none()
        )
        if prev_cycle == None:
            logging.error(f"{code} for {prev_school_year} not found")
            sys.exit(1)
        # Create an attendance cycle with the same month and day as last year's
        # but and incremented year
        year = datetime.timedelta(days=365)
        now = datetime.datetime.now()
        cycle = SchoolAttendanceCycle(
            school_year                = school_year,
            school_code                = school_code,
            code                       = code,
            description                = prev_cycle.description,
            end_date                   = prev_cycle.end_date + year,
            gb_description             = prev_cycle.gb_description,
            read_only                  = prev_cycle.read_only,
            seq                        = prev_cycle.seq,
            sifid                      = prev_cycle.sifid,
            start_date                 = prev_cycle.start_date + year,
            cycle_type                 = prev_cycle.cycle_type,
            created_by_portal_OID      = "",
            created_by_task_OID        = "",
            created_by_user_OID        = "",
            created_ip                 = "",
            created_on                 = now,
            last_updated_by_portal_OID = "",
            last_updated_by_task_OID   = "",
            last_updated_by_user_OID   = "",
            last_updated_ip            = "",
            last_updated_on            = now,
        )
    return cycle

async def create_update(Schoology, name, start_date, end_date):
    """
    Creates or updates a grading period on Schoology if needed
    """
    grading_period = Schoology.GradingPeriods.lookup(name)
    if grading_period == None:
        print(f"{name} does not exist, creating")
        await Schoology.GradingPeriods.create_gp(name, start_date, end_date)
    else:
        if (grading_period['start'] != start_date.isoformat() or
            grading_period['end'] != end_date.isoformat()):
            print(f"{name} needs to be updated, updating")
            await Schoology.GradingPeriods.update(grading_period['id'], name, start_date, end_date)

async def sync(environment, school_year):
    """
    Syncs up Schoology grading periods with Genesis semesters
    """
    async with schoology.Session(environment) as Schoology:
        tasks = []
        # FY (from MTHS)
        cycle = attendance_cycle('FY', 'MTHS', school_year)
        name = f"{school_year} FY"
        tasks.append(create_update(Schoology, name, cycle.start_date,
            cycle.end_date))

        # Everything else can differ by school
        semesters = ['S1', 'S2', 'Q1', 'Q2', 'Q3', 'Q4']
        for school_code in AR.school_codes:
            for semester in semesters:
                cycle = attendance_cycle(semester, school_code, school_year)
                name = f"{school_year} {school_code} {semester}"
                tasks.append(create_update(Schoology, name, cycle.start_date,
                    cycle.end_date))

        await asyncio.gather(*tasks)

if __name__ == '__main__':
    main()
