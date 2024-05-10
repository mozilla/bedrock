#!/bin/bash -xe

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# CRITICAL: Assumes that Django's DATABASE_URL is set to point to postgres
# CRITICAL: Assumes that the bedrock deployment has a copy of the sqlite database downloaded

# Usage ./bin/bootstrap-empty-postgres-database.sh

# 1. Set up the database with the full Django schema, but no data.
# Note that PROD_DETAILS_STORAGE needs to not be DB-backed for this
# initial load, to avoid a chicken-and-egg import situation
PROD_DETAILS_STORAGE=product_details.storage.PDFileStorage ./manage.py migrate

# 2. Run db update scripts to pull down the usual data sources
./bin/run-db-update.sh

# 3. Port the Contentful data (for the VPN Resource Center pages) from sqlite
# (Contentful sync is not enabled and doesn't work any more, but
# we can get the data from the sqlite db in the bedrock install)
DATABASE_URL=sqlite://./data/bedrock.db ./manage.py dumpdata contentful.contentfulentry -o /tmp/contentful_data.json

# ...and then load it in to postgres
./manage.py loaddata /tmp/contentful_data.json
