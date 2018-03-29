#!/bin/bash -xe

LOCAL_DB_UPDATE=$(echo "${LOCAL_DB_UPDATE:-false}" | tr '[:upper:]' '[:lower:]')
if [[ "$LOCAL_DB_UPDATE" == "true" ]]; then
    exec python bin/cron.py file db
else
    exec python bin/cron.py file
fi
