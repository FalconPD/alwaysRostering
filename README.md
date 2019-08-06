# alwaysRostering

This directory contains the alwaysRostering framework in, written in python. The
AR directory has modules for various services including Genesis, Professional
Growth (formerly MyLearningPlan), Schoology, Atlas, MAP, and Education City. AR
basically sets up an [sqlalchemy](https://www.sqlalchemy.org/) ORM of the
information on Genesis with custom methods that are useful for rostering. These
methods support operations that were difficult in the Genesis ReportWriter
system, including querying based on [roles](docs/roles.md) and classes, combining
co-teacher rosters, and tracking teachers that are away on leave.

In this directory you will find the following subdirectories and scripts:

## [Atlas](https://github.com/FalconPD/alwaysRostering/tree/master/Atlas)

This directory contains scripts for working with the
[Atlas curriculum management system](https://monroek12.rubiconatlas.org).

## cronjob.sh

This scripts is used as a cronjob on a Linux VM to keep certain services in-sync with Genesis nightly.

## [Education City](https://github.com/FalconPD/alwaysRostering/tree/master/Education%20City) - Work in Progress

This directory contains the beginnings of a script for syncing
[Education City](https://ec2.educationcity.com) accounts. 

## Genesis

### make_db.py

This script uses the AR Genesis module to create a database of the information
currently on Genesis. It runs reports on Genesis and stores the output in an
sqlite3 file. Reports are run asynchronously, although Genesis is configured
such that only one session can be active at a time from non-internal IPs.
## [MAP](https://github.com/FalconPD/alwaysRostering/tree/master/MAP)

Scripts for working with rosters in [NWEA MAP](https://teach.mapnwea.org)

## [Panorama Education](https://github.com/FalconPD/alwaysRostering/tree/master/Panorama%20Education)

Scripts to create rosters for SEL surveys.

## [PG](https://github.com/FalconPD/alwaysRostering/tree/master/PG) - Work in Progress

Scripts for pulling information from Frontline Professional Growth (formerly MyLearningPlan). 

## Schoology/sync_schoology.py

This script automatically syncs buildings, users, courses, and enrollments with
[Schoology](https://monroetownship.schoology.com).
