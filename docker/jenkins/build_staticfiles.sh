#!/bin/bash

set -euxo pipefail

python manage.py collectstatic --link --noinput -v 0
python docker/bin/softlinkstatic.py
