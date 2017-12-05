#!/bin/bash
set -ex
if [ ! -e ./manage.py ]; then
    # this does not support symlinks
    script_parent_dir=${0%/*}/..
    cd $script_parent_dir
fi

if [[ "$BRANCH_NAME" == "prod" ]]; then
    ENV_FILE=prod
else
    ENV_FILE=master
fi

honcho run --env "docker/envfiles/${ENV_FILE}.env" python manage.py migrate --noinput
honcho run --env "docker/envfiles/${ENV_FILE}.env" python manage.py update_sitemaps
honcho run --env "docker/envfiles/${ENV_FILE}.env" python bin/cron.py --run-once file db
