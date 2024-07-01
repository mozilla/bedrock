#!/bin/bash

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

set -exo pipefail

rm -rf ./static

# We need to build statics with Wagtail temporarily enabled, so that we
# get all the files collected that are needed for the CMS deployment to run.
# Specificially: django.contrb.admin is added to INSTALLED_APPS in CMS mode
# which is needed for django-rq's management UI and the main Django Admin

if [[ "$1" == "--nolink" ]]; then
    WAGTAIL_ENABLE_ADMIN=True python manage.py collectstatic --noinput -v 0
else
    WAGTAIL_ENABLE_ADMIN=True python manage.py collectstatic -l --noinput -v 0
    docker/bin/softlinkstatic.py
fi
