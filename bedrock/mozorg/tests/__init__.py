# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from contextlib import contextmanager

from django.test import TestCase as DjTestCase, TransactionTestCase as DjTransactionTestCase

from lib.l10n_utils import translation


class TestCase(DjTestCase):
    """Base class for Bedrock test cases."""

    @contextmanager
    def activate_locale(self, locale):
        """Context manager that temporarily activates a locale."""
        translation.activate(locale)
        yield
        translation.deactivate()


class TransactionTestCase(DjTransactionTestCase):
    """Base class for Bedrock test cases that need transaction management or autoid truncation."""

    @contextmanager
    def activate_locale(self, locale):
        """Context manager that temporarily activates a locale."""
        translation.activate(locale)
        yield
        translation.deactivate()
