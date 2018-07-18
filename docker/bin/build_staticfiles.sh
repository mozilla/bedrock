#!/bin/bash

set -exo pipefail

rm -rf ./static

if [[ "$1" == "--nolink" ]]; then
    python manage.py collectstatic --noinput -v 0
else
    python manage.py collectstatic -l --noinput -v 0
    docker/bin/softlinkstatic.py
fi
