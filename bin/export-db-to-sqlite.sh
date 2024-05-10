#!/bin/bash -xe

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Exports the postgres database to a sqlite file, which can be copied to the cloud bucket for consumption by web pods

# Usage:
# ./bin/export-db-to-sqlite.sh /path/to/output.db

# CRITICAL: requires DATABASE_URL in the environment



db-to-sqlite $DATABASE_URL $1 --all \
    --redact auth_user username \
    --redact auth_user email \
    --redact auth_user first_name \
    --redact auth_user last_name \
    --redact auth_user password \
