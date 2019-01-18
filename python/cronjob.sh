#!/bin/bash

export PYTHONPATH="/home/ryan/alwaysRostering/python"

DATE=`date -I`
GENESIS="databases/${DATE}-genesis.db"
LOG="logs/${DATE}.log"

function log {
    RUNTIME=`date`
    echo "${RUNTIME} - $1" >> ${LOG}
}

function run {
    log "Running: ${1}" 
    ${1} >> ${LOG} 2>&1
    if [ $? -ne 0 ]; then
        log "Non-zero exit status... stopping."
        exit $?
    fi
}

# Get the Genesis DB
# CHECK THE FILESIZE TO MAKE SURE YOU DOWNLOADED SOMETHING OTHERWISE
# THE SYNC UTILITIES WILL TRY TO SYNC WITH AN EMPTY DATABASE AND DELETE
# ALL USERS!!!
run "python ./Genesis/make_db.py ${GENESIS}"
MINSIZE=38000000
DBSIZE=$(wc -c < "${GENESIS}")
if [ ${DBSIZE} -lt ${MINSIZE} ]; then
    log "Genesis database file is too small... stopping."
    exit 1
fi

# Create and upload MAP rosters
run "python ./MAP/create_rosters.py ${GENESIS} MAP/rosters/${DATE} all"
STANDARD="MAP/rosters/${DATE}_StandardRoster.csv"
ADDITIONAL="MAP/rosters/${DATE}_AdditionalUsers.csv"
run "python ./MAP/upload_rosters.py --standard ${STANDARD} --additional ${ADDITIONAL} --status"

# Sync Atlas user accounts
run "python ./Atlas/sync_atlas.py ${GENESIS} ./Atlas/id_map.csv sync_users"

#date >> ${LOG}
#echo "=== Syncing Schoology ===" >> ${LOG}
#python ./Schoology/sync_schoology.py ${GENESIS} >> ${LOG} 2>&1
#

# Check on the status of the MAP import
run "python ./MAP/upload_rosters.py --status"
