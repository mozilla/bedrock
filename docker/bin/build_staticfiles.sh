#!/bin/bash

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

set -exo pipefail

rm -rf ./static

if [[ "$1" == "--nolink" ]]; then
    python manage.py collectstatic --noinput -v 0
else
    python manage.py collectstatic -l --noinput -v 0
    docker/bin/softlinkstatic.py
fi
