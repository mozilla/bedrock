# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
from math import floor

from django.test import RequestFactory
from django.utils.http import parse_http_date

from bedrock.mozorg.tests import TestCase
from bedrock.mozorg.tests import views


class ViewDecoratorTests(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def _test_cache_headers(self, view, hours):
        """
        Should have appropriate Cache-Control and Expires headers.
        """
        test_request = self.rf.get('/hi-there-dude/')
        resp = view(test_request)
        num_seconds = hours * 60 * 60
        self.assertEqual(resp['cache-control'], 'max-age=%d' % num_seconds)

        now_date = floor(time.time())
        exp_date = parse_http_date(resp['expires'])
        self.assertAlmostEqual(now_date + num_seconds, exp_date, delta=2)

    def test_cache_headers_48_hours(self):
        """
        Test a view that should be cached for 48 hours.
        """
        self._test_cache_headers(views.view_test_48_hrs, 48)

    def test_cache_headers_30_days(self):
        """
        Test a view that should be cached for 30 days.
        """
        self._test_cache_headers(views.view_test_30_days, 30 * 24)
