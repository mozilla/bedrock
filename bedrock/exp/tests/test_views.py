# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import ANY, patch

from django.test import override_settings
from django.test.client import RequestFactory

from bedrock.exp import views
from bedrock.mozorg.tests import TestCase


@override_settings(DEV=False)
@patch("bedrock.exp.views.l10n_utils.render")
class TestExpFirefoxNew(TestCase):
    def test_download_template(self, render_mock):
        req = RequestFactory().get("/exp/firefox/new/")
        req.locale = "en-US"
        views.new(req)
        render_mock.assert_called_once_with(req, "exp/firefox/new/download.html", ANY, ftl_files="firefox/new/desktop")
