#!/bin/bash -xe

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

ruff check .
black --check .
isort --check .
moz-l10n-lint l10n/l10n-pontoon.toml
moz-l10n-lint l10n/l10n-vendor.toml
moz-l10n-lint l10n-pocket/l10n-vendor.toml
python manage.py lint_ftl -q
python manage.py version
python manage.py migrate --noinput
py.test lib bedrock \
    --cov-config=.coveragerc \
    --cov-report=html \
    --cov-report=term-missing \
    --cov-report=xml:python_coverage/coverage.xml \
    --cov=.
py.test -r a tests/redirects
