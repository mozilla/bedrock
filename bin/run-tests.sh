#!/bin/bash -xe

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

ruff check .
ruff format --check .
moz-l10n-lint l10n/l10n-pontoon.toml
moz-l10n-lint l10n/l10n-vendor.toml
python manage.py lint_ftl -q
python manage.py version

# EXPECTED_DB_VENDOR is set by the test-image (sqlite) and test-image-postgres
# compose services, so that CI logs prove which backend is really in use and a
# misconfigured run cannot silently fall back to the default SQLite database.
if [[ -n "${EXPECTED_DB_VENDOR:-}" ]]; then
    python bin/check-db-backend.py
fi

python manage.py migrate --noinput
python manage.py makemigrations --check
# Set PYTEST_XDIST_WORKERS=0 to run the suite in a single process when debugging.
pytest lib bedrock \
    -n "${PYTEST_XDIST_WORKERS:-auto}" \
    --durations=30 \
    --cov-config=.coveragerc \
    --cov-report=html \
    --cov-report=term-missing \
    --cov-report=xml:python_coverage/coverage.xml \
    --cov=.
pytest -r a tests/redirects
