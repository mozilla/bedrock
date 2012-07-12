from contextlib import contextmanager
import unittest

from django.utils.translation import get_language

import test_utils
from tower import activate
from funfactory.urlresolvers import (get_url_prefix, Prefixer, set_url_prefix)


class TestCase(unittest.TestCase):
    """Base class for Bedrock test cases."""
    @contextmanager
    def activate(self, locale):
        """Context manager that temporarily activates a locale."""
        old_prefix = get_url_prefix()
        old_locale = get_language()
        rf = test_utils.RequestFactory()
        set_url_prefix(Prefixer(rf.get('/%s/' % (locale,))))
        activate(locale)
        yield
        set_url_prefix(old_prefix)
        activate(old_locale)
