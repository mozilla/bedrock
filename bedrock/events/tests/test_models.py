# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os.path
from datetime import datetime

from django.test.utils import override_settings

from mock import patch
from nose.tools import eq_

from bedrock.events.models import Event
from bedrock.mozorg.tests import TestCase


TEST_DATA = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                         'test_data')


class TestICalSync(TestCase):
    def test_sync_data(self):
        """Data should sync successfully."""
        with open(os.path.join(TEST_DATA, 'reps.ical')) as fh:
            Event.objects.sync_with_ical(fh.read())

        self.assertEqual(Event.objects.count(), 117)

        with open(os.path.join(TEST_DATA, 'reps_fewer.ical')) as fh:
            Event.objects.sync_with_ical(fh.read())

        self.assertEqual(Event.objects.count(), 14)


class TestFutureQuerySet(TestCase):
    @override_settings(USE_TZ=True)
    @patch('bedrock.events.models.datetime')
    def test_future_dst_use_tz(self, mock_datetime):
        """
        Should not raise error during DST change
        """
        mock_datetime.utcnow.return_value = datetime(2014, 11, 02, 01, 01)
        eq_(Event.objects.future().count(), 0)

    @override_settings(USE_TZ=False)
    @patch('bedrock.events.models.datetime')
    def test_future_dst(self, mock_datetime):
        """
        Should not raise error during DST change
        """
        mock_datetime.utcnow.return_value = datetime(2014, 11, 02, 01, 01)
        eq_(Event.objects.future().count(), 0)
