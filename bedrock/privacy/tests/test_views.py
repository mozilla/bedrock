# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import patch

from django.http import HttpResponse
from django.test.client import RequestFactory

from bedrock.mozorg.tests import TestCase
from bedrock.privacy import views


@patch("bedrock.firefox.views.l10n_utils.render", return_value=HttpResponse())
@patch.object(views.PrivacyDocView, "get_legal_doc")
class TestFirefoxTermsOfServiceDocView(TestCase):
    def test_default_template(self, render_mock, lld_mock):
        req = RequestFactory().get("/privacy/notices/firefox/")
        req.locale = "en-US"
        view = views.firefox_notices
        view(req)
        template = lld_mock.call_args[0][1]
        assert template == "privacy/notices/firefox.html"

    def test_tos_template(self, render_mock, lld_mock):
        req = RequestFactory().get("/privacy/notices/firefox/?v=product")
        req.locale = "en-US"
        view = views.firefox_notices
        view(req)
        template = lld_mock.call_args[0][1]
        assert template == "privacy/notices/firefox-tos.html"
