# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import patch

from django.http import HttpResponse
from django.test.client import RequestFactory

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
        assert template == "privacy/notices/firefox.html"

    def test_simple_template(self, render_mock, lld_mock):
        lld_mock.return_value["content"].select.return_value = None
        req = RequestFactory().get("/privacy/notices/firefox/?v=product")
        req.locale = "en-US"
        view = views.firefox_notices
        view(req)
        template = render_mock.call_args[0][1]
        assert template == "privacy/notices/firefox-simple.html"
