This directory contains a rewritten version of the alwaysRostering framework in
python. The AR directory has modules for various services including Genesis,
MyLearningPlan, and Schoology. AR basically sets up an
[sqlalchemy](https://www.sqlalchemy.org/) ORM of the information on Genesis
with custom methods that are useful for rostering. These methods include
querying Genesis data based on [roles](roles.md) and classes.

In this directory you will find the following scripts:

## make_db.py

This script uses the AR Genesis module to create a database of the information
currently on Genesis. It runs reports on Genesis and stores the output in an
sqlite3 file. Reports are run asynchronously, although Genesis is configured
such that only one session can be active at a time from non-internal IPs.

## sync_schoology.py

This script automatically syncs buildings, users, courses, and enrollments with
[Schoology](https://monroetownship.schoology.com).

## [Atlas](https://github.com/FalconPD/alwaysRostering/tree/master/python/Atlas)

This directory contains scripts for working with the
[Atlas curriculum management system](https://monroek12.rubiconatlas.org).

## [MAP](https://github.com/FalconPD/alwaysRostering/tree/master/python/MAP)

This directory contains scripts to create rosters for working with
[NWEA MAP](https://teach.mapnwea.org)
