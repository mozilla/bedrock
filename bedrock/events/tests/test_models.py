# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os.path

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
