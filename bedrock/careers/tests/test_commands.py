# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from datetime import datetime, timezone
from io import StringIO
from unittest.mock import Mock, patch

from django.core.management import call_command
from django.test.utils import override_settings

from bedrock.careers.models import Position
from bedrock.careers.tests import PositionFactory
from bedrock.mozorg.tests import TestCase

REQUESTS = "bedrock.careers.management.commands.sync_greenhouse.requests"


@override_settings(GREENHOUSE_BOARDS=["mozilla"])
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

    def test_semicolon_location_normalized_to_commas(self):
        """Greenhouse can join multiple locations with ';'; store comma-only."""
        jobs_response = {
            "jobs": [
                {
                    "id": "xxx",
                    "internal_job_id": 8223520,
                    "title": "Web Fox",
                    "absolute_url": "http://example.com/foo",
                    "updated_at": "2016-07-25T14:45:57-04:00",
                    "location": {"name": "Remote Belgium; Remote Denmark; Remote Finland"},
                },
            ]
        }
        with patch(REQUESTS) as requests:
            requests.get().json.return_value = jobs_response
            call_command("sync_greenhouse", stdout=StringIO())
        position = Position.objects.get()
        self.assertEqual(position.job_locations, "Remote Belgium, Remote Denmark, Remote Finland")

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

    @override_settings(GREENHOUSE_BOARDS=["mozilla", "mozillafoundation"])
    def test_multiple_boards(self):
        """Jobs from every configured board are fetched, and stale jobs are still removed."""

        def jobs_response(job_id, internal_job_id, title):
            return {
                "jobs": [
                    {
                        "id": job_id,
                        "internal_job_id": internal_job_id,
                        "title": title,
                        "absolute_url": f"http://example.com/{job_id}",
                        "updated_at": "2016-07-25T14:45:57-04:00",
                    },
                ]
            }

        responses = {
            "https://boards-api.greenhouse.io/v1/boards/mozilla/jobs?content=true": jobs_response("xxx", 99, "Web Fox"),
            "https://boards-api.greenhouse.io/v1/boards/mozillafoundation/jobs?content=true": jobs_response("yyy", 98, "Web Kangaroo"),
        }

        def get(url):
            response = Mock()
            response.json.return_value = responses[url]
            return response

        PositionFactory(job_id="zzz", internal_job_id=97)
        with patch(REQUESTS) as requests:
            requests.get.side_effect = get
            call_command("sync_greenhouse", stdout=StringIO())

        self.assertEqual(requests.get.call_count, 2)
        for url in responses:
            requests.get.assert_any_call(url)
        # Jobs from both boards remain, and the job no longer listed by either board is removed.
        self.assertEqual(sorted(Position.objects.values_list("job_id", flat=True)), ["xxx", "yyy"])

    def test_missing_internal_job_id_uses_job_id(self):
        """Postings without an internal_job_id are grouped by their own job ID, not collapsed together."""
        jobs_response = {
            "jobs": [
                {
                    "id": 111,
                    "internal_job_id": None,
                    "title": "Web Fox",
                    "absolute_url": "http://example.com/foo",
                    "updated_at": "2016-07-25T14:45:57-04:00",
                },
                {
                    "id": 222,
                    "internal_job_id": None,
                    "title": "Web Kangaroo",
                    "absolute_url": "http://example.com/bar",
                    "updated_at": "2016-07-25T14:45:57-04:00",
                },
            ]
        }
        with patch(REQUESTS) as requests:
            requests.get().json.return_value = jobs_response
            call_command("sync_greenhouse", stdout=StringIO())
        positions = Position.objects.all()
        self.assertEqual(positions.count(), 2)
        self.assertEqual(sorted(p.internal_job_id for p in positions), [111, 222])

    def test_other_source_positions_are_not_removed(self):
        """Positions from a source other than Greenhouse are left alone by the cleanup step."""
        PositionFactory(job_id="legacy", internal_job_id=5, source="legacy", apply_url="http://example.com/legacy")
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
        self.assertTrue(Position.objects.filter(job_id="legacy", source="legacy").exists())

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
