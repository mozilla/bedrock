#!/bin/sh

./docker/run-common.sh
./manage.py runserver 0.0.0.0:8000
