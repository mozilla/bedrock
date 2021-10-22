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

if [[ ! -f .env ]]; then
    cp .env-dist .env
fi

# get fresh database
./bin/run-db-download.py --force

# get fresh l10n files
./manage.py l10n_update
