#!/bin/bash
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

set -ex
if [ ! -e ./manage.py ]; then
    # this does not support symlinks
    script_parent_dir=${0%/*}/..
    cd $script_parent_dir
fi

# Check whether --retain-db was passed
DO_DB_DOWNLOAD=true
for arg in "$@"; do
  if [ "$arg" == "--retain-db" ]; then
    DO_DB_DOWNLOAD=false
    break
  fi
done

if [ "$DO_DB_DOWNLOAD" = true ]; then
    ./bin/run-db-download.py --force
else
    echo "Skipping DB download"
fi

./manage.py migrate --noinput
./manage.py l10n_update

if [[ -n "${DEMO_SERVER_ADMIN_USERS}" ]]; then
    ./manage.py bootstrap_demo_server_admins
fi
