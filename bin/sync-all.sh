#!/bin/bash
set -ex
if [ ! -e ./manage.py ]; then
    # this does not support symlinks
    script_parent_dir=${0%/*}/..
    cd $script_parent_dir
fi

./bin/run-db-download.py --force
./manage.py migrate --noinput
./manage.py l10n_update
