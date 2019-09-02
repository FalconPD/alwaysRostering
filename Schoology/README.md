# Schoology Scripts

This directory contains scripts for working with the
[Schoology LMS](https://monroetownship.schoology.com). All scripts are meant to
be run in the base pipenv (run `pipenv shell` from the main directory). Scripts
are broken into smaller functions to support fractional updating that occurs
during the summer time before the schedule is released.

## buildings.py

```console
Usage: buildings.py [OPTIONS] DB_FILE

  Syncs up Schoology buildings with a Genesis Database

  DB_FILE - A sqlite3 file of the Genesis database

Options:
  -e, --environment TEXT  [default: testing]
  -d, --debug             Print debugging statements
  --help                  Show this message and exit.
```

## courses.py

```console
Usage: courses.py [OPTIONS] DB_FILE

  Syncs up Schoology courses with a Genesis Database

  DB_FILE - A sqlite3 file of the Genesis database

Options:
  -e, --environment TEXT  [default: testing]
  -d, --debug             Print debugging statements
  --help                  Show this message and exit.
```

## enrollments.py

```console
Usage: enrollments.py [OPTIONS] DB_FILE

  Adds Schoology enrollments based on sections in a Genesis Database

  DB_FILE - A sqlite3 file of the Genesis database

Options:
  -e, --environment TEXT  [default: testing]
  -d, --debug             Print debugging statements
  --help                  Show this message and exit.
```

## extra_scripts/

This directory contains scripts that were designed for one-time use or testing.

## grading_periods.py

```console
Usage: grading_periods.py [OPTIONS] DB_FILE SCHOOL_YEAR

  Syncs Schoology grading periods with Genesis semesters. Currently syncs FY
  for the whole district and S1, S2, Q1, Q2, Q3, Q4 for each building. Uses
  dates from a previous year if the current year cannot be found.

  DB_FILE - A sqlite3 file of the Genesis database
  SCHOOL_YEAR - School year to sync, ex. 2018-19

Options:
  -e, --environment TEXT  [default: testing]
  -d, --debug
  --help                  Show this message and exit.
```

## old/

This directory contains old scripts that may still be referenced.

## users.py

Syncs staff and students in Genesis with user accounts in Schoology. Assigns
roles based on the Genesis job codes and assigns advisors to students that have
the `counselor_id` attribute set.

```console
Usage: users.py [OPTIONS] DB_FILE

  Syncs up Schoology users with a Genesis Database

  DB_FILE - A sqlite3 file of the Genesis database

Options:
  -e, --environment TEXT  [default: testing]
  -d, --debug             Print debugging statements
  -f, --force             Perform possibly dangerous actions
  --help                  Show this message and exit.
```
