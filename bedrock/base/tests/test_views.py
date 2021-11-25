# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import datetime
from unittest.mock import patch

from django.test import RequestFactory, TestCase
from django.utils.timezone import now as tz_now

import pytest

from bedrock.base.views import GeoTemplateView, get_contentful_sync_info
from bedrock.contentful.models import ContentfulEntry

geo_template_view = GeoTemplateView.as_view(
    geo_template_names={
        "DE": "firefox-klar.html",
        "GB": "firefox-focus.html",
    },
    template_name="firefox-mobile.html",
)


class TestGeoTemplateView(TestCase):
    def get_template(self, country):
        with patch("bedrock.firefox.views.l10n_utils.render") as render_mock:
            with patch("bedrock.base.views.get_country_from_request") as geo_mock:
                geo_mock.return_value = country
                rf = RequestFactory()
                req = rf.get("/")
                geo_template_view(req)
                return render_mock.call_args[0][1][0]

    def test_country_template(self):
        template = self.get_template("DE")
        assert template == "firefox-klar.html"

    def test_default_template(self):
        template = self.get_template("US")
        assert template == "firefox-mobile.html"

    def test_no_country(self):
        template = self.get_template(None)
        assert template == "firefox-mobile.html"


@pytest.mark.django_db
def test_get_contentful_sync_info():

    middle = tz_now()
    first = middle - datetime.timedelta(hours=3)
    last = middle + datetime.timedelta(hours=3)

    for idx, timestamp in enumerate([middle, last, first]):
        ContentfulEntry.objects.create(
            contentful_id=f"id-{idx}",
            last_modified=timestamp,
        )

    assert get_contentful_sync_info() == {
        "latest_sync": last,
    }

    ContentfulEntry.objects.all().delete()
    assert get_contentful_sync_info() == {
        "latest_sync": None,
    }
