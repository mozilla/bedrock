#!/bin/bash

set -euxo pipefail

python manage.py collectstatic -l --noinput -v 0
docker/bin/softlinkstatic.py
