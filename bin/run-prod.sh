#!/bin/bash -xe

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

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

granian --interface wsgi \
    --host 0.0.0.0 \
    --port "${PORT:-8000}" \
    --no-ws \
    --workers "${WSGI_NUM_WORKERS:-8}" \
    wsgi.app:application
