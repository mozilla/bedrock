#!/bin/sh

./docker/run-common.sh
gunicorn wsgi.app:application -b 0.0.0.0:${PORT:-8000} -w 2 --error-logfile - --access-logfile - --log-level ${LOGLEVEL:-info}
