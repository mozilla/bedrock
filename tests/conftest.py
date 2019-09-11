# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from django.db.backends.sqlite3.base import BaseDatabaseWrapper as SQLiteWrapper


# pytest-django is currently broken by attempting to set the read only
# property ``allow_thread_sharing`` (as of Django 2.2), so work around
# that.
def mutable_allow_thread_sharing(self, allow):
    if allow:
        if not self.allow_thread_sharing:
            self.inc_thread_sharing()


SQLiteWrapper.allow_thread_sharing = property(
    SQLiteWrapper.allow_thread_sharing.__get__, mutable_allow_thread_sharing)


@pytest.fixture(scope='session')
def base_url(base_url, request):
    return base_url or request.getfixturevalue('live_server').url
