#!/usr/bin/env sh -e

cd "$(dirname "$0")"

source env.sh

if [ ! -f db.sqlite3 ]; then
    cat create-db.sql | sqlite3 db.sqlite3
fi

./_run_workflow.py \
--board-id 111 \
--db-file db.sqlite3 \
--log-base-folder log/ \
--range yesterday
#--trend-thread-id XXXX