#!/bin/bash

# always exit on an error
set -e

# show all commands as they run
set -x

# Get the Genesis DB
# CHECK THE FILESIZE TO MAKE SURE YOU DOWNLOADED SOMETHING OTHERWISE
# THE SYNC UTILITIES WILL TRY TO SYNC WITH AN EMPTY DATABASE AND DELETE
# ALL USERS!!!
pipenv run python ./Genesis/make_db.py genesis.db
MINSIZE=38000000
DBSIZE=$(wc -c < genesis.db)
if [ ${DBSIZE} -lt ${MINSIZE} ]; then
    echo "Genesis database file is too small... stopping."
    exit 1
fi

# Create MAP rosters
pipenv run python ./MAP/create_rosters.py genesis.db MAP all

# Upload the MAP StandardRoster
pipenv run python ./MAP/upload_rosters.py --standard MAP_StandardRoster.csv --status

# Uploading MAP rosters takes a while so we perform some other actions before
# uploading the MAP AdditionalUsers roster

# Sync Schoology users accounts
pipenv run python ./Schoology/users.py --environment=production genesis.db

# Sync Schoology courses
pipenv run python ./Schoology/courses.py --environment=production genesis.db

# Sync Schoology enrollments
pipenv run python ./Schoology/enrollments.py --environment=production genesis.db

# Sync Atlas users
pipenv run python ./Atlas/users.py genesis.db

# Upload the MAP AdditionalUsers
pipenv run python ./MAP/upload_rosters.py --additional MAP_AdditionalUsers.csv --status
