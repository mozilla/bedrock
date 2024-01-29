#!/bin/bash -xe

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

function run-uwsgi () {
    if [[ -z "$NEW_RELIC_LICENSE_KEY" ]]; then
        exec uwsgi "$@"
    else
        export NEW_RELIC_CONFIG_FILE=newrelic.ini
        exec newrelic-admin run-program uwsgi "$@"
    fi
}

# look for the required files and fail quickly if it's not there
STARTUP_FILES=(
    "data/bedrock.db"
    "data/last-run-update_locales"
    "data/last-run-download_database"
)
for fname in "${STARTUP_FILES[@]}"; do
    if [[ ! -f "$fname" ]]; then
        echo "$fname not found";
        exit 1
    fi
done

run-uwsgi --ini /app/wsgi/uwsgi.ini
