# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
from unittest.mock import ANY, patch

from django.conf import settings
from django.test import RequestFactory

from bedrock.mozorg.tests import TestCase
from bedrock.mozorg.util import get_fb_like_locale, page

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_files")


class TestGetFacebookLikeLocale(TestCase):
    def test_supported_locale(self):
        """
        Return the given locale if supported.
        """
        assert get_fb_like_locale("en-PI") == "en_PI"

    def test_first_supported_locale_for_language(self):
        """
        If the given locale is not supported, iterate through
        the supported locales and return the first one that
        matches the language.
        """
        assert get_fb_like_locale("es-AR") == "es_ES"

    def test_unsupported_locale(self):
        """
        Return the default en_US when locale isn't supported.
        """
        assert get_fb_like_locale("zz-ZZ") == "en_US"


@patch("bedrock.mozorg.util.l10n_utils")
class TestPageUtil(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def test_locale_redirect(self, l10n_mock):
        """Should use l10n render."""
        url = page("walter/abides/", "walter/abides.html", donny="ashes")
        url.callback(self.rf.get("/walter/abides/"))
        l10n_mock.render.assert_called_with(ANY, "walter/abides.html", {"urlname": "walter.abides", "donny": "ashes"}, ftl_files=None)

    def test_locale_redirect_works_home_page(self, l10n_mock):
        """Make sure the home page still works. "/" is a special case."""
        url = page("", "index.html")
        url.callback(self.rf.get("/"))
        l10n_mock.render.assert_called_with(ANY, "index.html", {"urlname": "index"}, ftl_files=None)

    def test_url_name_set_from_template(self, l10n_mock):
        """If not provided the URL pattern name should be set from the template path."""
        url = page("lebowski/urban_achievers/", "lebowski/achievers.html")
        assert url.name == "lebowski.achievers"

    def test_url_name_set_from_param(self, l10n_mock):
        """If provided the URL pattern name should be set from the parameter."""
        url = page("lebowski/urban_achievers/", "lebowski/achievers.html", url_name="proud.we.are.of.all.of.them")
        assert url.name == "proud.we.are.of.all.of.them"

    def test_url_pattern_no_slash(self, l10n_mock):
        "The url route should pass through unchanged"
        url = page("dude/abides.json", "dude/abides.html", donny="ashes")
        assert str(url.pattern) == "dude/abides.json"


class TestProdLocales(TestCase):
    def test_no_dupes(self):
        # Make sure we didn't duplicate a locale in more than one region.
        assert set.intersection(*[set(locales) for locales in settings.LOCALES_BY_REGION.values()]) == set()

    def test_inclusive(self):
        # Make sure all locales are included in `PROD_LANGUAGES`.
        # We add 1 for the "ja-JP-mac" exception.
        assert sum([len(locales) for locales in settings.LOCALES_BY_REGION.values()]) + 1 == len(settings.PROD_LANGUAGES)
