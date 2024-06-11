# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from django.core.management import call_command

import pytest


@pytest.mark.django_db
def test_no_missing_migrations():
    "Unit test to confirm that we're not missing any migrations"

    error_message = "We are missing a Django Migration. Please run ./manage.py makemigrations --dry-run to see what is missing"

    try:
        call_command("makemigrations", "--check")
    except SystemExit as se:
        if se.code == 1:
            pytest.fail(error_message)
        else:
            # If something else is up, we don't want to ignore it
            raise se
