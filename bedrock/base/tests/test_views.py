import json
from unittest.mock import patch

from django.test import TestCase, RequestFactory
from django.test import override_settings

from bedrock.base.views import geolocate, GeoRedirectView, GeoTemplateView


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


geo_view = GeoRedirectView.as_view(
    geo_urls={
        "CA": "firefox.new",
        "US": "firefox",
    },
    default_url="https://abide.dude",
)


@override_settings(DEV=False)
class TestGeoRedirectView(TestCase):
    def get_response(self, country):
        with patch("bedrock.base.views.get_country_from_request") as geo_mock:
            geo_mock.return_value = country
            rf = RequestFactory()
            req = rf.get("/")
            return geo_view(req)

    def test_special_country(self):
        resp = self.get_response("CA")
        assert resp.status_code == 302
        assert resp["location"] == "/firefox/new/"

        resp = self.get_response("US")
        assert resp.status_code == 302
        assert resp["location"] == "/firefox/"

    def test_other_country(self):
        resp = self.get_response("DE")
        assert resp.status_code == 302
        assert resp["location"] == "https://abide.dude"

        resp = self.get_response("JA")
        assert resp.status_code == 302
        assert resp["location"] == "https://abide.dude"

    def test_invalid_country(self):
        resp = self.get_response("dude")
        assert resp.status_code == 302
        assert resp["location"] == "https://abide.dude"

        resp = self.get_response("42")
        assert resp.status_code == 302
        assert resp["location"] == "https://abide.dude"


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
