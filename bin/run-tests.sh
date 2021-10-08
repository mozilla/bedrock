#!/bin/bash -xe

flake8
black --check .
isort . --check
moz-l10n-lint l10n/l10n-pontoon.toml
moz-l10n-lint l10n/l10n-vendor.toml
python manage.py lint_ftl -q
python manage.py runscript check_calendars
python manage.py version
python manage.py migrate --noinput
py.test lib bedrock
py.test -r a tests/redirects
