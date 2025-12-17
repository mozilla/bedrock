# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import patch

from django.http import HttpResponse
from django.test.client import RequestFactory

from waffle.models import Switch
from waffle.testutils import override_switch

from bedrock.mozorg.tests import TestCase
from bedrock.privacy import views


@patch.object(views.PrivacyDocView, "get_legal_doc")
@patch("bedrock.firefox.views.l10n_utils.render", return_value=HttpResponse())
class TestFirefoxSimpleDocView(TestCase):
    def test_default_template(self, render_mock, lld_mock):
        lld_mock.return_value["content"].select.return_value = None
        req = RequestFactory().get("/privacy/notices/firefox/")
        req.locale = "en-US"
        view = views.firefox_notices
        view(req)
        template = render_mock.call_args[0][1]
        assert template == "privacy/notices/firefox-intro.html"

    def test_simple_template(self, render_mock, lld_mock):
        lld_mock.return_value["content"].select.return_value = None
        req = RequestFactory().get("/privacy/notices/firefox/?v=product")
        req.locale = "en-US"
        view = views.firefox_notices
        view(req)
        template = render_mock.call_args[0][1]
        assert template == "privacy/notices/firefox-simple.html"


@patch.object(views.PrivacyDocView, "get_legal_doc")
@patch("bedrock.firefox.views.l10n_utils.render", return_value=HttpResponse())
class TestFocusSimpleDocView(TestCase):
    def test_default_template(self, render_mock, lld_mock):
        lld_mock.return_value["content"].select.return_value = None
        req = RequestFactory().get("/privacy/notices/firefox-focus/")
        req.locale = "en-US"
        view = views.firefox_focus_notices
        view(req)
        template = render_mock.call_args[0][1]
        assert template == "privacy/notices/firefox.html"

    def test_simple_template(self, render_mock, lld_mock):
        lld_mock.return_value["content"].select.return_value = None
        req = RequestFactory().get("/privacy/notices/firefox-focus/?v=product")
        req.locale = "en-US"
        view = views.firefox_focus_notices
        view(req)
        template = render_mock.call_args[0][1]
        assert template == "privacy/notices/firefox-simple.html"


class TestFirefoxPrivacyNextViewBehaviour(TestCase):
    def test_redirect_happens_when_switch_is_not_defined(self):
        assert not Switch.objects.filter(name="ENABLE_FIREFOX_PRIVACY_NEXT").exists()
        resp = self.client.get("/en-US/privacy/firefox/next/")
        assert resp.status_code == 302
        assert resp.headers["location"] == "/en-US/privacy/firefox/"

    def test_redirect_happens_when_switch_is_OFF(self):
        with override_switch("ENABLE_FIREFOX_PRIVACY_NEXT", active=False):
            resp = self.client.get("/en-US/privacy/firefox/next/")
            assert resp.status_code == 302
            assert resp.headers["location"] == "/en-US/privacy/firefox/"

    @patch.object(views.PrivacyDocView, "get_legal_doc")
    @patch("bedrock.firefox.views.l10n_utils.render", return_value=HttpResponse())
    def test_redirect_does_not_happen_when_switch_is_ON(self, render_mock, lld_mock):
        with override_switch("ENABLE_FIREFOX_PRIVACY_NEXT", active=True):
            lld_mock.return_value["content"].select.return_value = None
            resp = self.client.get("/en-US/privacy/firefox/next/")
            assert resp.status_code == 200
            assert render_mock.call_args_list[0][0][1] == "privacy/notices/firefox-intro.html"

    def test_uses_correct_view_class(self):
        assert isinstance(views.firefox_notices_preview.view_class(), views.FirefoxPrivacyPreviewDocView)
