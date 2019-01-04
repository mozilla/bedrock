#!/bin/bash
set -ex
if [ ! -e ./manage.py ]; then
    # this does not support symlinks
    script_parent_dir=${0%/*}/..
    cd $script_parent_dir
fi

case "$BRANCH_NAME" in
    "stage" | "prod") ENV_FILE=prod ;;
    *) ENV_FILE=master ;;
esac

# use honcho to inject the proper env vars
honcho run --env "docker/envfiles/${ENV_FILE}.env" ./bin/sync-all.sh
