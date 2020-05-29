#!/bin/bash
set -ex
if [ ! -e ./manage.py ]; then
    # this does not support symlinks
    script_parent_dir=${0%/*}/..
    cd $script_parent_dir
fi

# ensure the data dir exists
mkdir -p data

# use honcho to inject the proper env vars
honcho run --env docker/envfiles/prod.env ./bin/sync-all.sh
