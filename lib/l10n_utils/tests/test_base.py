# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
from unittest.mock import ANY, Mock, call, patch

from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings

import pytest
from django_jinja.backend import Jinja2

from lib import l10n_utils

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_files")
TEMPLATE_DIRS = (os.path.join(ROOT, "templates"),)
jinja_env = Jinja2.get_default()


@patch.object(jinja_env.env.loader, "searchpath", TEMPLATE_DIRS)
@override_settings(
    ROOT=ROOT,
    DEV=False,
    ROOT_URLCONF="lib.l10n_utils.tests.test_files.urls",
)
class TestRender(TestCase):
    def _test(self, path, template, locale, accept_lang, status, destination=None, active_locales=None, add_active_locales=None):
        request = RequestFactory().get(path)
        request.META["HTTP_ACCEPT_LANGUAGE"] = accept_lang
        request.locale = locale
        ctx = {}
        if active_locales:
            ctx["active_locales"] = active_locales

        if add_active_locales:
            ctx["add_active_locales"] = add_active_locales

        response = l10n_utils.render(request, template, ctx)

        if status == 302:
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response["Location"], destination)
            self.assertEqual(response["Vary"], "Accept-Language")
        else:
            self.assertEqual(response.status_code, 200)

    def test_firefox(self):
        path = "/firefox/new/"
        template = "firefox/new.html"
        locales = ["en-US", "en-GB", "fr", "es-ES"]

        # No locale changes needed when we're given a valid locale
        self._test(path, template, "en-US", "en-us,en;q=0.5", 302, "/en-US/firefox/new/", active_locales=locales)

        # en-GB is activated on /firefox/new/
        self._test(path, template, "en-GB", "en-gb,en;q=0.5", 302, "/en-GB/firefox/new/", active_locales=locales)

        # fr-FR should be treated as fr
        self._test(path, template, "fr-FR", "fr-fr", 302, "/fr/firefox/new/", active_locales=locales)

        # Should fallback to the user's second preferred language
        self._test(path, template, "zu", "zu,fr;q=0.7,en;q=0.3", 302, "/fr/firefox/new/", active_locales=locales)

        # Should fallback to one of the site's fallback languages
        self._test(path, template, "es-CL", "es-CL,es;q=0.7,en;q=0.3", 302, "/es-ES/firefox/new/", active_locales=locales)

        # Should use the user's base language (en-CA -> en) if no exact matches
        self._test(path, template, "en-CA", "en-CA,fr", 302, "/en-US/firefox/new/", active_locales=locales)

    def test_add_active_locales(self):
        # expect same results as above, but with locales from `add_active_locales`
        path = "/firefox/new/"
        template = "firefox/new.html"
        locales = ["en-US", "en-GB", "fr", "es-ES"]

        # No locale changes needed when we're given a valid locale
        self._test(path, template, "en-US", "en-us,en;q=0.5", 302, "/en-US/firefox/new/", add_active_locales=locales)

        # en-GB is activated on /firefox/new/
        self._test(path, template, "en-GB", "en-gb,en;q=0.5", 302, "/en-GB/firefox/new/", add_active_locales=locales)

        # fr-FR should be treated as fr
        self._test(path, template, "fr-FR", "fr-fr", 302, "/fr/firefox/new/", add_active_locales=locales)

        # Should fallback to the user's second preferred language
        self._test(path, template, "zu", "zu,fr;q=0.7,en;q=0.3", 302, "/fr/firefox/new/", add_active_locales=locales)

        # Should fallback to one of the site's fallback languages
        self._test(path, template, "es-CL", "es-CL,es;q=0.7,en;q=0.3", 302, "/es-ES/firefox/new/", add_active_locales=locales)

    def test_ftl_files_unmodified(self):
        """A list passed to the ftl_files parameter should not be modified in place"""
        ftl_files = ["dude", "walter"]
        path = "/firefox/new/"
        template = "firefox/new.html"
        req = RequestFactory().get(path)
        l10n_utils.render(req, template, ftl_files=ftl_files)
        assert ftl_files == ["dude", "walter"]

    @patch.object(l10n_utils, "django_render")
    @patch.object(l10n_utils, "ftl_active_locales")
    def test_activation_files(self, fal_mock, dr_mock):
        ftl_files = ["dude", "walter"]
        path = "/firefox/new/"
        template = "firefox/new.html"
        activation_files = ftl_files + [template]
        req = RequestFactory().get(path)
        l10n_utils.render(req, template, activation_files=activation_files)
        fal_mock.assert_has_calls(
            [
                call("dude"),
                call("walter"),
            ],
            any_order=True,
        )


class TestGetAcceptLanguages(TestCase):
    def _test(self, accept_lang, list):
        request = RequestFactory().get("/")
        request.META["HTTP_ACCEPT_LANGUAGE"] = accept_lang
        self.assertEqual(l10n_utils.get_accept_languages(request), list)

    def test_valid_lang_codes(self):
        """
        Should return a list of valid lang codes
        """
        self._test("fr-FR", ["fr-fr"])
        self._test("en-us,en;q=0.5", ["en-us", "en"])
        self._test("pt-pt,fr;q=0.8,it-it;q=0.5,de;q=0.3", ["pt-pt", "fr", "it-it", "de"])
        self._test("ja-JP-mac,ja-JP;q=0.7,ja;q=0.3", ["ja-jp-mac", "ja-jp", "ja"])
        self._test("foo,bar;q=0.5", ["foo", "bar"])
        # Verify the return lang codes are ordered by rank.
        self._test("de;q=0.5,en-us", ["en-us", "de"])

    def test_invalid_lang_codes(self):
        """
        Should return a list of valid lang codes or an empty list
        """
        self._test("", [])
        self._test("en_us,en*;q=0.5", [])
        self._test("Chinese,zh-cn;q=0.5", ["chinese", "zh-cn"])


@patch.object(l10n_utils, "render")
class TestL10nTemplateView(TestCase):
    def setUp(self):
        self.req = RequestFactory().get("/")

    def test_post(self, render_mock):
        view = l10n_utils.L10nTemplateView.as_view(template_name="post.html", ftl_files="dude")
        resp = view(RequestFactory().post("/"))
        self.assertEqual(resp.status_code, 405)

    def test_ftl_files(self, render_mock):
        view = l10n_utils.L10nTemplateView.as_view(template_name="dude.html", ftl_files="dude")
        view(self.req)
        render_mock.assert_called_with(self.req, ["dude.html"], ANY, ftl_files="dude", activation_files=None)

    def test_ftl_files_map(self, render_mock):
        view = l10n_utils.L10nTemplateView.as_view(template_name="dude.html", ftl_files_map={"dude.html": "dude"})
        view(self.req)
        render_mock.assert_called_with(self.req, ["dude.html"], ANY, ftl_files="dude", activation_files=None)
        # no match means no FTL files
        view = l10n_utils.L10nTemplateView.as_view(template_name="dude.html", ftl_files_map={"donny.html": "donny"})
        view(self.req)
        render_mock.assert_called_with(self.req, ["dude.html"], ANY, ftl_files=None, activation_files=None)

    def test_ftl_activations(self, render_mock):
        view = l10n_utils.L10nTemplateView.as_view(template_name="dude.html", ftl_files="dude", activation_files=["dude", "donny"])
        view(self.req)
        render_mock.assert_called_with(self.req, ["dude.html"], ANY, ftl_files="dude", activation_files=["dude", "donny"])


@patch.object(l10n_utils, "_get_language_map", Mock(return_value={"an": "an", "de": "de", "en": "en-US", "en-us": "en-US", "fr": "fr"}))
@pytest.mark.parametrize(
    "translations, accept_languages, expected",
    (
        # Anything with a 'en-US' transtion and 'en' root accept languages, goes to 'en-US'.
        (["en-US"], ["en-US"], "en-US"),
        (["en-US"], ["en-CA"], "en-US"),
        (["en-US"], ["en"], "en-US"),
        (["en-US", "de"], ["en-GB"], "en-US"),
        # Anything with a 'en-US' transtion and unsupported translations, goes to 'en-US' by default.
        (["en-US"], ["zu"], "en-US"),
        (["en-US"], ["fr"], "en-US"),
        (["en-US", "de"], ["fr"], "en-US"),
        # The user's prioritized accept language should be chosen first.
        (["en-US", "de"], ["de", "en-US"], "de"),
        (["en-US", "de", "fr"], ["fr", "de"], "fr"),
        (["en-US", "de", "fr"], ["en-CA", "fr", "de"], "en-US"),
        # A request for only inactive translations should default to 'en-US'. Bug 1752823
        (["am", "an", "en-US"], ["mk", "gu-IN"], "en-US"),
        # "am" is not a valid language in the list of PROD_LANGUAGES
        (["am", "an"], ["mk", "gu-IN"], "an"),
    ),
)
def test_get_best_translation(translations, accept_languages, expected):
    assert l10n_utils.get_best_translation(translations, accept_languages) == expected
