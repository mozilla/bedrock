#!/bin/bash -xe

flake8
python manage.py lint_ftl -q
python manage.py runscript check_calendars
python manage.py version
python manage.py migrate --noinput
py.test lib bedrock
py.test -r a tests/redirects
