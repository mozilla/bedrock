#!/bin/bash -xe

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

bin/run-db-download.py --force
LOCAL_DB_UPDATE=$(echo "${LOCAL_DB_UPDATE:-false}" | tr '[:upper:]' '[:lower:]')
if [[ "$LOCAL_DB_UPDATE" == "true" ]]; then
    python manage.py migrate --noinput
    exec python bin/cron.py file db
else
    exec python bin/cron.py file
fi
