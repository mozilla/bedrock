#!/bin/bash
set -ex
if [ ! -e ./manage.py ]; then
    # this does not support symlinks
    script_parent_dir=${0%/*}/..
    cd $script_parent_dir
fi
./manage.py migrate --noinput
./manage.py update_sitemaps
./bin/cron.py --run-once
