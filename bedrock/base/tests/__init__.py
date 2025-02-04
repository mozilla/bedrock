# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from contextlib import contextmanager

from django.test import TestCase as DjTestCase

from lib.l10n_utils import translation


class TestCase(DjTestCase):
    """Base class for Springfield test cases."""

    @contextmanager
    def activate_locale(self, locale):
        """Context manager that temporarily activates a locale."""
        translation.activate(locale)
        yield
        translation.deactivate()
