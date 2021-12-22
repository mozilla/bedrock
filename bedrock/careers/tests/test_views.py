# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import datetime

from django.urls import reverse
from django.utils import timezone

from bedrock.careers.forms import PositionFilterForm
from bedrock.careers.tests import PositionFactory
from bedrock.mozorg.tests import TestCase
from bedrock.wordpress.models import BlogPost


class PositionTests(TestCase):
    def test_context(self):
        response = self.client.get(reverse("careers.listings"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context["form"]), type(PositionFilterForm()))

    def test_position_case_sensitive_match(self):
        """
        Validate that a position match is returned from a case-sensitive job id and it doesn't
        raise a multiple records error.
        """
        job_id_1 = "oflWVfwb"
        job_id_2 = "oFlWVfwB"
        PositionFactory(job_id=job_id_1)
        PositionFactory(job_id=job_id_2)

        url = reverse("careers.position", kwargs={"job_id": job_id_1, "source": "gh"})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["position"].job_id, job_id_1)

        url = reverse("careers.position", kwargs={"job_id": job_id_2, "source": "gh"})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["position"].job_id, job_id_2)

    def test_position_view_404_uses_custom_template(self):
        url = reverse("careers.position", kwargs={"job_id": "aabbccdd", "source": "gh"})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "careers/404.html")


class BlogTests(TestCase):
    blog_data = {
        "wp_blog_slug": "careers",
        "excerpt": "",
        "link": "",
    }

    def _populate_blog_posts(self):
        today = timezone.now()
        older1 = timezone.now() - datetime.timedelta(days=1)
        older2 = timezone.now() - datetime.timedelta(days=2)

        recent_today = BlogPost.objects.create(wp_id=1, date=today, modified=today, title="Post 1", tags=["Growth"], **self.blog_data)
        recent_older1 = BlogPost.objects.create(wp_id=2, date=older1, modified=older1, title="Post 2", tags=["Inclusion"], **self.blog_data)
        recent_older2 = BlogPost.objects.create(wp_id=3, date=older2, modified=older2, title="Post 3", tags=["Life"], **self.blog_data)
        return (recent_today, recent_older1, recent_older2)

    def test_blog_posts_none_featured(self):
        recent_today, recent_older1, recent_older2 = self._populate_blog_posts()

        response = self.client.get(reverse("careers.home"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["featured_post"], None)
        # Coerse to a list, not a `QuerySet`.
        self.assertEqual(list(response.context["recent_posts"]), [recent_today, recent_older1, recent_older2])

    def test_blog_posts_featured(self):
        recent_today, recent_older1, recent_older2 = self._populate_blog_posts()

        # Posts tagged "Story" show up in the featured position.
        featured = BlogPost.objects.create(
            wp_id=99, date=timezone.now(), modified=timezone.now(), title="Post Featured", tags=["Story"], **self.blog_data
        )

        response = self.client.get(reverse("careers.home"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["featured_post"], featured)
        # Coerse to a list, not a `QuerySet`.
        self.assertEqual(list(response.context["recent_posts"]), [recent_today, recent_older1])
