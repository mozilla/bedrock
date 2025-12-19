#!/bin/bash -xe

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# CRITICAL: Assumes that Django's DATABASE_URL is set to point to *Postgres*
# CRITICAL: Assumes that the bedrock deployment has a copy of the sqlite database downloaded

# Usage ./bin/fill-empty-postgres-database.sh

# 0. Are we configured appropriately?
ACTIVE_DATABASE=$(PROD_DETAILS_STORAGE=product_details.storage.PDFileStorage python manage.py shell -c "from django.conf import settings; print(settings.DATABASES['default']['ENGINE'])")

if [[ $ACTIVE_DATABASE != *"postgres"* ]]; then
    echo "ERROR: Django's active database does not point to a Postgres database."
    exit 100
fi

# 1. Set up the database with the full Django schema, but no data.
# Note that PROD_DETAILS_STORAGE needs to not be DB-backed for this
# initial load, to avoid a chicken-and-egg import situation
PROD_DETAILS_STORAGE=product_details.storage.PDFileStorage ./manage.py migrate

# 2. Run db update scripts to pull down the usual data sources
./bin/run-db-update.sh
