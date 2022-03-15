# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.urls import reverse

from bedrock.careers.tests import PositionFactory
from bedrock.mozorg.tests import TestCase


class FeedTests(TestCase):
    def test_career_feed(self):
        job_id_1 = "oflWVfwb"
        job_id_1_1 = "oflWVfwbb"  # Using an internal job ID to join these two.
        job_id_2 = "oFlWVfwB"
        job_id_3 = "oFlWVfwc"
        job_1 = PositionFactory(job_id=job_id_1, internal_job_id=999)
        job_1_1 = PositionFactory(job_id=job_id_1_1, internal_job_id=999)
        job_2 = PositionFactory(job_id=job_id_2)

        url = reverse("careers.feed")
        response = self.client.get(url, follow=True)
        self.assertEqual(response["Content-Type"], "application/rss+xml; charset=utf-8")
        self.assertEqual(response.status_code, 200)

        content = response.content.decode("utf-8")
        self.assertIn(reverse("careers.listings"), content)
        self.assertIn(url, content)

        for job in [job_1, job_2]:
            self.assertIn(job.title, content)
            self.assertIn(job.description, content)
            self.assertIn(job.department, content)
            self.assertIn(job.updated_at.strftime("%a, %d %b %Y %H:%M:%S %z"), content)
            self.assertIn(job.get_absolute_url(), content)
            self.assertNotIn("Worldwide", content)

        # Only the first job grouped with an internal job ID is shown in the feed.
        self.assertNotIn(job_1_1.get_absolute_url(), content)

        PositionFactory(job_id=job_id_3, location="Remote")
        response = self.client.get(url, follow=True)
        content = response.content.decode("utf-8")
        self.assertIn("Worldwide", content)
