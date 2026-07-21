#!/bin/bash -xe

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# look for the required files and fail quickly if it's not there
STARTUP_FILES=(
    "data/last-run-update_locales"
)
# If DATABASE_URL is defined, that means we're using Postgres not sqlite.
# However, if DATABASE_URL is NOT defined, we need SQLite-related files at startup
if [[ -z "$DATABASE_URL" ]]; then
    STARTUP_FILES+=("data/last-run-download_database")
    STARTUP_FILES+=("data/bedrock.db")
fi

for fname in "${STARTUP_FILES[@]}"; do
    if [[ ! -f "$fname" ]]; then
        echo "$fname not found";
        exit 1
    fi
done

# Granian recommends containerized apps use the defaults of workers=1, blocking-threads=1.
# We configure Granian to 1 worker and 1 blocking thread per pod, and let k8s manage the scaling.
#
# Adjust using these environment variables:
#   PORT: port to run the app on
#   GRANIAN_WORKERS: number of workers
#   GRANIAN_BLOCKING_THREADS: number of blocking threads
#   GRANIAN_LOG_LEVEL: log level to use (granian default: info)

granian --interface wsgi \
    --host 0.0.0.0 \
    --port "${PORT:-8000}" \
    --no-ws \
    wsgi.app:application
