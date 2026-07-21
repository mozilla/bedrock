# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from datetime import datetime, timezone
from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test.utils import override_settings

from bedrock.careers.models import Position
from bedrock.careers.tests import PositionFactory
from bedrock.mozorg.tests import TestCase

REQUESTS = "bedrock.careers.management.commands.sync_greenhouse.requests"


@override_settings(GREENHOUSE_BOARD="mozilla")
class SyncGreenhouseTests(TestCase):
    def test_job_fetch(self):
        jobs_response = {
            "jobs": [
                {
                    "id": "xxx",
                    "internal_job_id": 1234,
                    "title": "Web Fox",
                    "updated_at": "2016-07-25T14:45:57-04:00",
                    "absolute_url": "http://example.com/foo",
                    "content": "&lt;h2&gt;foo&lt;/h2&gt; bar",
                    "metadata": [{"id": 69450, "name": "Employment Type", "value": "Full-time", "value_type": "single_select"}],
                    "departments": [{"id": 13585, "name": "Engineering"}],
                    "location": {"name": "Remote US"},
                    "offices": [
                        {
                            "id": 1,
                            "name": "Greece",
                        },
                        {
                            "id": 2,
                            "name": "Remote",
                        },
                        {
                            "id": 3,
                            "name": "Portland",
                        },
                    ],
                },
            ]
        }
        with patch(REQUESTS) as requests:
            requests.get().json.return_value = jobs_response
            call_command("sync_greenhouse", stdout=StringIO())
        position = Position.objects.get()
        self.assertEqual(position.job_id, "xxx")
        self.assertEqual(position.internal_job_id, 1234)
        self.assertEqual(position.title, "Web Fox")
        self.assertEqual(position.updated_at, datetime(2016, 7, 25, 18, 45, 57, tzinfo=timezone.utc))
        self.assertEqual(position.location_list, ["Greece", "Portland", "Remote"])
        self.assertEqual(position.job_locations, "Remote US")
        self.assertEqual(position.department, "Engineering")
        self.assertEqual(position.apply_url, "http://example.com/foo")
        self.assertEqual(position.source, "gh")
        self.assertEqual(position.position_type, "Full-time")
        self.assertEqual(position.description, "<h4>foo</h4> bar")

    def test_job_removal(self):
        PositionFactory(job_id="xxx", internal_job_id=99)
        PositionFactory(job_id="yyy", internal_job_id=99)
        jobs_response = {
            "jobs": [
                {
                    "id": "xxx",
                    "internal_job_id": 99,
                    "title": "Web Fox",
                    "absolute_url": "http://example.com/foo",
                    "updated_at": "2016-07-25T14:45:57-04:00",
                },
            ]
        }
        with patch(REQUESTS) as requests:
            requests.get().json.return_value = jobs_response
            call_command("sync_greenhouse", stdout=StringIO())
        self.assertEqual(Position.objects.all().count(), 1)
        self.assertEqual(Position.objects.all()[0].job_id, "xxx")

    def test_position_description_none(self):
        """
        Store empty string is Greenhouse returns None for position or description.
        """
        jobs_response = {
            "jobs": [
                {
                    "id": "xxx",
                    "internal_job_id": 99,
                    "title": "Web Fox",
                    "absolute_url": "http://example.com/foo",
                    "updated_at": "2016-07-25T14:45:57-04:00",
                },
            ]
        }
        with patch(REQUESTS) as requests:
            requests.get().json.return_value = jobs_response
            call_command("sync_greenhouse", stdout=StringIO())
        self.assertEqual(Position.objects.all().count(), 1)
        self.assertEqual(Position.objects.all()[0].position_type, "")
        self.assertEqual(Position.objects.all()[0].description, "")

    def test_position_is_mofo(self):
        jobs_response = {
            "jobs": [
                {
                    "id": "xxx",
                    "internal_job_id": 99,
                    "title": "Web Fox",
                    "departments": [{"name": "Mozilla Foundation"}],
                    "absolute_url": "http://example.com/foo",
                    "updated_at": "2016-07-25T14:45:57-04:00",
                },
            ]
        }
        with patch(REQUESTS) as requests:
            requests.get().json.return_value = jobs_response
            call_command("sync_greenhouse", stdout=StringIO())
        self.assertEqual(Position.objects.all().count(), 1)
        self.assertEqual(Position.objects.all()[0].is_mofo, True)

    def test_position_is_moco(self):
        jobs_response = {
            "jobs": [
                {
                    "id": "xxx",
                    "internal_job_id": 99,
                    "title": "Web Fox",
                    "departments": [{"name": "Mozilla Foundation"}],
                    "absolute_url": "http://example.com/foo",
                    "updated_at": "2016-07-25T14:45:57-04:00",
                },
            ]
        }
        with patch(REQUESTS) as requests:
            requests.get().json.return_value = jobs_response
            call_command("sync_greenhouse", stdout=StringIO())
        self.assertEqual(Position.objects.all().count(), 1)
        self.assertEqual(Position.objects.all()[0].is_moco, False)

        jobs_response = {
            "jobs": [
                {
                    "id": "xxx",
                    "internal_job_id": 99,
                    "title": "Web Fox",
                    "departments": [{"name": "Marketing"}],
                    "absolute_url": "http://example.com/foo",
                    "updated_at": "2016-07-25T14:45:57-04:00",
                },
            ]
        }
        with patch(REQUESTS) as requests:
            requests.get().json.return_value = jobs_response
            call_command("sync_greenhouse", stdout=StringIO())
        self.assertEqual(Position.objects.all().count(), 1)
        self.assertEqual(Position.objects.all()[0].is_moco, True)

        jobs_response = {
            "jobs": [
                {
                    "id": "xxx",
                    "internal_job_id": 99,
                    "title": "Web Fox",
                    "departments": [{"name": "MZLA/Thunderbird"}],
                    "absolute_url": "http://example.com/foo",
                    "updated_at": "2016-07-25T14:45:57-04:00",
                },
            ]
        }
        with patch(REQUESTS) as requests:
            requests.get().json.return_value = jobs_response
            call_command("sync_greenhouse", stdout=StringIO())
        self.assertEqual(Position.objects.all().count(), 1)
        self.assertEqual(Position.objects.all()[0].is_moco, False)

    def test_repeat_job_ids(self):
        jobs_response = {
            "jobs": [
                {
                    "id": "xxx",
                    "internal_job_id": 99,
                    "title": "Web Fox",
                    "absolute_url": "http://example.com/foo",
                    "updated_at": "2016-07-25T14:45:57-04:00",
                },
                {
                    "id": "xxx",
                    "internal_job_id": 99,
                    "title": "Web Fox",
                    "absolute_url": "http://example.com/foo",
                    "updated_at": "2016-07-25T14:45:57-04:00",
                },
            ]
        }
        with patch(REQUESTS) as requests:
            requests.get().json.return_value = jobs_response
            call_command("sync_greenhouse", stdout=StringIO())
        self.assertEqual(Position.objects.all().count(), 1)

    def test_metadata_is_none(self):
        jobs_response = {
            "jobs": [
                {
                    "id": "xxx",
                    "internal_job_id": 99,
                    "title": "Web Fox",
                    "metadata": None,
                    "absolute_url": "http://example.com/foo",
                    "updated_at": "2016-07-25T14:45:57-04:00",
                },
            ]
        }
        with patch(REQUESTS) as requests:
            requests.get().json.return_value = jobs_response
            call_command("sync_greenhouse", stdout=StringIO())
        self.assertEqual(Position.objects.all().count(), 1)

    def test_xss_script_tags_removed(self):
        """Script tags and their content should be removed from job descriptions."""
        jobs_response = {
            "jobs": [
                {
                    "id": "xxx",
                    "internal_job_id": 99,
                    "title": "Web Fox",
                    "content": "&lt;p&gt;Hello&lt;/p&gt;&lt;script&gt;alert('xss')&lt;/script&gt;",
                    "absolute_url": "http://example.com/foo",
                    "updated_at": "2016-07-25T14:45:57-04:00",
                },
            ]
        }
        with patch(REQUESTS) as requests:
            requests.get().json.return_value = jobs_response
            call_command("sync_greenhouse", stdout=StringIO())
        position = Position.objects.get()
        self.assertIn("<p>Hello</p>", position.description)
        self.assertNotIn("<script>", position.description)
        self.assertNotIn("alert('xss')", position.description)

    def test_xss_javascript_urls_stripped(self):
        """javascript: URLs should be stripped from href attributes."""
        jobs_response = {
            "jobs": [
                {
                    "id": "xxx",
                    "internal_job_id": 99,
                    "title": "Web Fox",
                    "content": "&lt;a href=\"javascript:alert('xss')\"&gt;click me&lt;/a&gt;",
                    "absolute_url": "http://example.com/foo",
                    "updated_at": "2016-07-25T14:45:57-04:00",
                },
            ]
        }
        with patch(REQUESTS) as requests:
            requests.get().json.return_value = jobs_response
            call_command("sync_greenhouse", stdout=StringIO())
        position = Position.objects.get()
        self.assertNotIn("javascript:", position.description.lower())

    def test_xss_event_handlers_stripped(self):
        """Event handler attributes like onclick should be stripped."""
        jobs_response = {
            "jobs": [
                {
                    "id": "xxx",
                    "internal_job_id": 99,
                    "title": "Web Fox",
                    "content": "&lt;div onclick=\"alert('xss')\"&gt;content&lt;/div&gt;",
                    "absolute_url": "http://example.com/foo",
                    "updated_at": "2016-07-25T14:45:57-04:00",
                },
            ]
        }
        with patch(REQUESTS) as requests:
            requests.get().json.return_value = jobs_response
            call_command("sync_greenhouse", stdout=StringIO())
        position = Position.objects.get()
        self.assertNotIn("onclick", position.description.lower())

    def test_valid_urls_preserved(self):
        """Valid http/https URLs should be preserved."""
        jobs_response = {
            "jobs": [
                {
                    "id": "xxx",
                    "internal_job_id": 99,
                    "title": "Web Fox",
                    "content": '&lt;a href="https://example.com"&gt;link&lt;/a&gt;',
                    "absolute_url": "http://example.com/foo",
                    "updated_at": "2016-07-25T14:45:57-04:00",
                },
            ]
        }
        with patch(REQUESTS) as requests:
            requests.get().json.return_value = jobs_response
            call_command("sync_greenhouse", stdout=StringIO())
        position = Position.objects.get()
        self.assertIn('href="https://example.com"', position.description)
