# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import patch

from django.http import HttpResponse
from django.test.client import RequestFactory

from bedrock.legal import views
from bedrock.legal_docs import views as legal_docs_views
from bedrock.mozorg.tests import TestCase


@patch("bedrock.firefox.views.l10n_utils.render", return_value=HttpResponse())
@patch.object(legal_docs_views, "load_legal_doc")
class TestFirefoxSimpleDocView(TestCase):
    def test_default_template(self, render_mock, lld_mock):
        req = RequestFactory().get("/about/legal/terms/firefox/")
        req.locale = "en-US"
        view = views.FirefoxTermsOfServiceDocView.as_view()
        view(req)
        template = lld_mock.call_args[0][1]
        assert template == "legal/terms/firefox.html"

    def test_simple_template(self, render_mock, lld_mock):
        req = RequestFactory().get("/about/legal/terms/firefox/?v=product")
        req.locale = "en-US"
        view = views.FirefoxTermsOfServiceDocView.as_view()
        view(req)
        template = lld_mock.call_args[0][1]
        assert template == "legal/terms/firefox-simple.html"
