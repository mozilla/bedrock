#!/bin/bash

set -xe

./docker/run-common.sh

venv/bin/python manage.py get_geoip_db

server=${WSGI_SERVER:-gunicorn}
if [[ $server == "gunicorn" ]]
then
    venv/bin/gunicorn wsgi.app:application -b 0.0.0.0:${PORT:-8000} -w 2 --error-logfile - --access-logfile - --log-level ${LOGLEVEL:-info}
elif [[ $server == "uwsgi" ]]
then
    venv/bin/uwsgi --master --wsgi wsgi.app:application --http 0.0.0.0:${PORT:-8000}
else
    >&2 echo "Unknown wsgi server $server"
fi
