# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.template.loader import render_to_string
from django.test import RequestFactory, TestCase, override_settings

import jinja2

from bedrock.base.context_processors import i18n
from lib.l10n_utils import translation


class TestContext(TestCase):
    def setUp(self):
        translation.activate("en-US")
        self.factory = RequestFactory()
        translation.activate("en-US")

    def render(self, content, request=None):
        if not request:
            request = self.factory.get("/")
        tpl = jinja2.Template(content)
        return render_to_string(tpl, request=request)

    def test_request(self):
        assert self.render("{{ request.path }}") == "/"

    def test_settings(self):
        assert self.render("{{ settings.LANGUAGE_CODE }}") == "en-US"

    def test_languages(self):
        assert self.render("{{ LANGUAGES[-1][1] }}") == settings.LANGUAGES[-1][1]

    def test_lang_setting(self):
        assert self.render("{{ LANG }}") == "en-US"

    def test_lang_dir(self):
        assert self.render("{{ DIR }}") == "ltr"

    def test_geo_header(self):
        """Country code from request header should work"""
        req = self.factory.get("/", HTTP_CF_IPCOUNTRY="de")
        assert self.render("{{ country_code }}", req) == "DE"

    @override_settings(DEV=False)
    def test_geo_no_header(self):
        """Country code when header absent should be None"""
        req = self.factory.get("/")
        assert self.render("{{ country_code }}", req) == "None"

    def test_geo_param(self):
        """Country code from header should be overridden by query param
        for pre-prod domains."""
        req = self.factory.get("/", data={"geo": "fr"}, HTTP_CF_IPCOUNTRY="de")
        assert self.render("{{ country_code }}", req) == "FR"

        # should use header if at prod domain
        req = self.factory.get("/", data={"geo": "fr"}, HTTP_CF_IPCOUNTRY="de", HTTP_HOST="www.mozilla.org")
        assert self.render("{{ country_code }}", req) == "DE"

    @override_settings(DEV=False)
    def test_invalid_geo_param(self):
        req = self.factory.get("/", data={"geo": "france"}, HTTP_CF_IPCOUNTRY="de")
        assert self.render("{{ country_code }}", req) == "DE"

        req = self.factory.get("/", data={"geo": ""}, HTTP_CF_IPCOUNTRY="de")
        assert self.render("{{ country_code }}", req) == "DE"

        req = self.factory.get("/", data={"geo": "france"})
        assert self.render("{{ country_code }}", req) == "None"

    def test_canonical_lang_equals_lang_normally(self):
        """CANONICAL_LANG should equal LANG when there is no content_locale on the request."""
        translation.activate("fr")
        req = self.factory.get("/fr/page/")
        ctx = i18n(req)
        assert ctx["LANG"] == "fr"
        assert ctx["CANONICAL_LANG"] == "fr"

    def test_canonical_lang_uses_content_locale(self):
        """CANONICAL_LANG uses request.content_locale when set (alias locale serving)."""
        translation.activate("pt-PT")
        req = self.factory.get("/pt-PT/page/")
        req.content_locale = "pt-BR"
        ctx = i18n(req)
        assert ctx["LANG"] == "pt-PT"
        assert ctx["CANONICAL_LANG"] == "pt-BR"
