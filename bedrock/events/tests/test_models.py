# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from builtins import object
import os.path
from datetime import date, datetime

from django.test.utils import override_settings

from mock import patch
from pytz import utc

from bedrock.events.models import Event, calendar_id_from_google_url, calendar_url_for_event
from bedrock.mozorg.tests import TestCase


TEST_DATA = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                         'test_data')
GCAL_ID = 'mozilla.com_l9g7ie050ngr3g4qv6bgiinoig%40group.calendar.google.com'
GCAL_URL = 'https://www.google.com/calendar/ical/mozilla.com_l9g7ie050ngr3g4qv6bgiinoig' \
           '%40group.calendar.google.com/public/basic.ics'


class TestICalHelperFunctions(TestCase):
    def test_calendar_id_from_google_url(self):
        """Should get calendar ID from a google calendar ical feed URL."""
        self.assertEqual(calendar_id_from_google_url(GCAL_URL), GCAL_ID)

    def test_calendar_url_for_event(self):
        class FakeEvent(object):
            start_time = date(2015, 7, 10)
            end_time = date(2015, 7, 20)

        event_url = calendar_url_for_event(FakeEvent(), GCAL_ID)
        self.assertIn('dates=20150710%2f20150720', event_url)
        self.assertIn('src=' + GCAL_ID, event_url)


class TestICalSync(TestCase):
    def test_sync_data(self):
        """Data should sync successfully."""
        with patch('bedrock.events.models.utcnow',
                   return_value=datetime(2013, 10, 1, tzinfo=utc)):
            with open(os.path.join(TEST_DATA, 'reps.ical')) as fh:
                Event.objects.sync_with_ical(fh.read(), 'https://example.com')

        self.assertEqual(Event.objects.count(), 117)

        with patch('bedrock.events.models.utcnow',
                   return_value=datetime(2014, 12, 1, tzinfo=utc)):
            Event.objects.past().delete()

        self.assertEqual(Event.objects.count(), 12)

    def test_google_cal_no_url(self):
        """URL for event should be to the gcal if no url specified."""
        # Security Days 2014
        with patch('bedrock.events.models.utcnow',
                   return_value=datetime(2013, 10, 1, tzinfo=utc)):
            with open(os.path.join(TEST_DATA, 'reps.ical')) as fh:
                Event.objects.sync_with_ical(fh.read(), GCAL_URL)

        evnt = Event.objects.get(title='Security Days 2014')
        self.assertIn('www.google.com/calendar/embed', evnt.url)
        evnt = Event.objects.get(title='Ada Lovelace IT Day')
        self.assertNotIn('www.google.com/calendar/embed', evnt.url)


class TestFutureQuerySet(TestCase):
    @override_settings(USE_TZ=True)
    @patch('bedrock.events.models.datetime')
    def test_future_dst_use_tz(self, mock_datetime):
        """
        Should not raise error during DST change
        """
        mock_datetime.utcnow.return_value = datetime(2014, 11, 0o2, 0o1, 0o1)
        assert Event.objects.future().count() == 0

    @override_settings(USE_TZ=False)
    @patch('bedrock.events.models.datetime')
    def test_future_dst(self, mock_datetime):
        """
        Should not raise error during DST change
        """
        mock_datetime.utcnow.return_value = datetime(2014, 11, 0o2, 0o1, 0o1)
        assert Event.objects.future().count() == 0


@override_settings(USE_TZ=False)
class TestQuerySets(TestCase):
    fixtures = ['events']

    def setUp(self):
        datetime_patcher = patch('bedrock.events.models.datetime')
        self.mock_datetime = datetime_patcher.start()
        self.addCleanup(datetime_patcher.stop)

        self.mock_datetime.utcnow.return_value = datetime(2015, 0o5, 0o4, 12, 00)

    def test_past(self):
        """
        Should return events with end_date less than patched now
        """
        assert Event.objects.past().count() == 2

    def test_current_and_future(self):
        """
        Should return events with end_date greater than patched now
        """
        assert Event.objects.current_and_future().count() == 2

    def test_future(self):
        """
        Should return events with start_date greater than patched now
        """
        assert Event.objects.future().count() == 1
