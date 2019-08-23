# grading_periods.py

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

# sync_schoology.py

Syncs Genesis users, classes, buildings, and enrollments with Schoology. This
script is in the process of being broken into smaller, more manageable scripts.

```console
Usage: sync_schoology.py [OPTIONS] DB_FILE

  Syncs up Schoology with a Genesis Database

  DB_FILE - A sqlite3 file of the Genesis database

Options:
  --debug  Print debugging statements
  --help   Show this message and exit.
```

# users.py

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
