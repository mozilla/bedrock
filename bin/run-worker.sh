#!/bin/bash -ex

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program \
python manage.py rqworker default image_renditions --max-jobs "${RQ_MAX_JOBS:-5000}"
