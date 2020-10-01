#!/bin/bash -xe

python bin/run-db-download.py --force
python manage.py migrate --noinput
exec python bin/cron.py db
