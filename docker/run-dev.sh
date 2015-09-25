#!/bin/sh

./docker/run-common.sh
venv/bin/python manage.py runserver 0.0.0.0:8000
