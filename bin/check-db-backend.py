#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Fail fast unless Django is really connected to the expected database backend.

CI runs the same suite twice - once against SQLite and once against PostgreSQL.
This check makes the backend that is actually in use explicit in the logs, so a
misconfigured run can never silently fall back to the default SQLite database.

Usage:
    EXPECTED_DB_VENDOR=postgresql python bin/check-db-backend.py
    EXPECTED_DB_VENDOR=sqlite python bin/check-db-backend.py
"""

import os
import sys
from pathlib import Path

import django

# When run as a script, Python puts this file's directory (bin/) on sys.path
# rather than the repo root, so add the root to make `bedrock` importable.
sys.path.append(str(Path(__file__).resolve().parents[1]))


def main():
    expected = os.environ.get("EXPECTED_DB_VENDOR", "").strip()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bedrock.settings")
    django.setup()

    from django.db import connection

    connection.ensure_connection()
    db_settings = connection.settings_dict
    actual = connection.vendor
    print(
        "Database backend check: "
        f"expected={expected or '(any)'} actual={actual} "
        f"host={db_settings['HOST']} port={db_settings['PORT']} name={db_settings['NAME']}"
    )
    if expected and actual != expected:
        sys.exit(f"ERROR: expected a {expected} database but Django is connected to {actual}")

    print("Database backend check: OK")


if __name__ == "__main__":
    main()
