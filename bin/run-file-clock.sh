#!/bin/bash -xe

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# On demos, we don't want to download the latest DB, else we'll lose CMS data
# Also skip if using PostgreSQL (DATABASE_URL set)
SKIP_FORCED_DB_DOWNLOAD=$(echo "${SKIP_FORCED_DB_DOWNLOAD:-false}" | tr '[:upper:]' '[:lower:]')
if [[ "$SKIP_FORCED_DB_DOWNLOAD" == "false" && -z "$DATABASE_URL" ]]; then
    bin/run-db-download.py --force
fi

LOCAL_DB_UPDATE=$(echo "${LOCAL_DB_UPDATE:-false}" | tr '[:upper:]' '[:lower:]')
if [[ "$LOCAL_DB_UPDATE" == "true" ]]; then
    python manage.py migrate --noinput
    exec python bin/cron.py file db
else
    exec python bin/cron.py file
fi
