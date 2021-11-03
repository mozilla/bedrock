# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
from unittest.mock import patch

from django.test import RequestFactory, TestCase

from bedrock.base.views import GeoTemplateView, geolocate


class TestGeolocate(TestCase):
    def get_country(self, country):
        with patch("bedrock.base.views.get_country_from_request") as geo_mock:
            geo_mock.return_value = country
            rf = RequestFactory()
            req = rf.get("/")
            resp = geolocate(req)
            return json.loads(resp.content)

    def test_geo_returns(self):
        self.assertDictEqual(self.get_country("US"), {"country_code": "US"})
        self.assertDictEqual(self.get_country("FR"), {"country_code": "FR"})
        self.assertDictEqual(
            self.get_country(None),
            {
                "error": {
                    "errors": [
                        {
                            "domain": "geolocation",
                            "reason": "notFound",
                            "message": "Not found",
                        }
                    ],
                    "code": 404,
                    "message": "Not found",
                }
            },
        )


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
