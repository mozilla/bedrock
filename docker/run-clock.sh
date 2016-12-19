#!/bin/bash -xe

python manage.py migrate --noinput --database bedrock
exec python bin/cron.py db
