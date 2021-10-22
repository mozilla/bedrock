#!/bin/bash -xe

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# ensure the app will start while run from supervisor
# mostly for demos
STARTUP_FILES=(
    "data/last-run-update_locales"
    "data/last-run-download_database"
)
for fname in "${STARTUP_FILES[@]}"; do
    touch "$fname"
done

exec supervisord -c etc/supervisord.conf
