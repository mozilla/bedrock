# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import patch

from django.conf import settings
from django.test import RequestFactory, TestCase

import pytest

from bedrock.base.views import GeoTemplateView, page_gone_view, page_not_found_view, server_error_view

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


class TestErrorPages(TestCase):
    """Test error page handlers by calling them directly with mocked dependencies."""

    def check_error_handler(self, handler_func, expected_template, expected_status=200):
        with patch("lib.l10n_utils.render") as render_mock:
            rf = RequestFactory()
            req = rf.get("/")

            try:
                handler_func(req, exception=None)
            except TypeError:
                handler_func(req)

            args, kwargs = render_mock.call_args
            self.assertEqual(args[1], expected_template)
            self.assertEqual(kwargs.get("status"), expected_status)

    def test_404_handler(self):
        """Test 404 handler uses correct template and status."""
        self.check_error_handler(page_not_found_view, "404.html", 404)

    def test_410_handler(self):
        """Test 410 handler uses correct template and status."""
        self.check_error_handler(page_gone_view, "410.html", 410)

    def test_500_handler(self):
        """Test 500 handler uses correct template and status."""
        self.check_error_handler(server_error_view, "500.html", 500)


@pytest.mark.django_db
def test_csrf_view_is_custom_one():
    assert settings.CSRF_FAILURE_VIEW == "bedrock.base.views.csrf_failure"
