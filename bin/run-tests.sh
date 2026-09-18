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

if [[ "${EXPECTED_DB_VENDOR:-}" == "postgresql" ]]; then
    # WORKAROUND, not a fix: on a *virgin* PostgreSQL database the cms data
    # migrations create pages before the wagtailsearch tables exist, and on
    # PostgreSQL the failed index write aborts the whole migration transaction
    # (SQLite tolerates it). Pre-creating just those tables lets the normal
    # `migrate` below complete, which is all the throwaway CI database needs.
    # This does NOT address the underlying migration dependency problem - doing
    # that properly (e.g. declaring the wagtailsearch dependency on cms.0005, or
    # not indexing while migrations run) is a decision for the maintainers.
    python manage.py migrate wagtailsearch --noinput
fi

python manage.py migrate --noinput
python manage.py makemigrations --check
pytest lib bedrock \
    --cov-config=.coveragerc \
    --cov-report=html \
    --cov-report=term-missing \
    --cov-report=xml:python_coverage/coverage.xml \
    --cov=.
pytest -r a tests/redirects
