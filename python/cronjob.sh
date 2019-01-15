#!/bin/sh

export PYTHONPATH="/home/ryan/alwaysRostering/python"

DATE=`date -I`
GENESIS="databases/${DATE}-genesis.db"
python ./Genesis/make_db.py ${GENESIS}
python ./Atlas/sync_atlas.py ${GENESIS} ./Atlas/id_map.csv sync_users
python ./Schoology/sync_schoology.py ${GENESIS}
python ./MAP/create_rosters.py ${GENESIS} MAP/rosters/${DATE} all 
