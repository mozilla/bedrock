# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import sys

from .base import *  # noqa
try:
    from .local import *  # noqa
except ImportError as exc:
    exc.args = tuple(['%s (did you rename bedrock/settings/local.py-dist?)' %
                      exc.args[0]])
    raise exc


if DEV:
    ALLOWED_HOSTS = ['*']


# Any databases configured other than "default" should be
# read-only slaves, which funfactory's default router
# should use with this setting.
if 'manage.py' not in sys.argv:
    SLAVE_DATABASES = [db for db in DATABASES if db != 'default']


MEDIA_URL = CDN_BASE_URL + MEDIA_URL
