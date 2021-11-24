# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from sentry_sdk import capture_exception


def alert_sentry_on_exception(cls):
    """Custom decorator for management commands that ensure failures
    anywhere in the main handle() call get to Sentry.

    Usage:

        @alert_sentry_on_exception
        class MyTestManagementCommand(BaseCommand):
            ...
    """

    def _handle(cls, *args, **kwargs):
        try:
            cls.old_handle(*args, **kwargs)
        except Exception as ex:
            capture_exception(ex)
            # We DO want the exception to bubble up, because a calling script
            # will want to check the exit code
            raise

    cls.old_handle = cls.handle  # Will fail hard if the subclass lacks handle(), but that's good
    cls.handle = _handle

    return cls
