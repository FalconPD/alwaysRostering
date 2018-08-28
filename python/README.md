This directory contains a rewritten version of the alwaysRostering framework in python. The AR directory has modules for various services including Genesis, MyLearningPlan, and Schoology. AR basically sets up an sqlalchemy ORM of the information on Genesis with custom methods that are useful for rostering.

In this directory you will find the following scripts:

## make_db.py

This script uses the AR Genesis module to create a database of the information currently on Genesis. It runs reports on Genesis and stores the output in an sqlite3 file. Reports are run asynchronously, although Genesis is configured such that only one session can be active at a time.
