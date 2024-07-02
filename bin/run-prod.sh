#!/bin/bash -xe

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# look for the required files and fail quickly if it's not there
STARTUP_FILES=(
    "data/last-run-update_locales"
    "data/last-run-download_database"
)
# If DATABASE_URL is defined, that means we're using Postgres not sqlite.
# However, if DATABASE_URL is NOT defined, we need to be sure the sqlite DB file
# is already present at startup
if [[ -z "$DATABASE_URL" ]]; then
    STARTUP_FILES+=("data/bedrock.db")
fi

for fname in "${STARTUP_FILES[@]}"; do
    if [[ ! -f "$fname" ]]; then
        echo "$fname not found";
        exit 1
    fi
done

# Granian recommends containerized apps use the defaults of workers=1, threads=1.
# The backgpressure defaults to backlog (1024) / workers (1), but should be adjusted to match the
# number of database connections when configured for databases.
granian --interface wsgi \
    --host 0.0.0.0 \
    --port "${PORT:-8000}" \
    --no-ws \
    --workers "${GRANIAN_WORKERS:-1}" \
    --threads "${GRANIAN_THREADS:-1}" \
    --backpressure "${GRANIAN_BACKPRESSURE:-1024}" \
    --log-level "${GRANIAN_LOG_LEVEL:-warning}" \
    wsgi.app:application
