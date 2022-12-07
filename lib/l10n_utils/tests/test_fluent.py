# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from pathlib import Path
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase, override_settings

from lib.l10n_utils import fluent, translation

L10N_PATH = Path(__file__).with_name("test_files").joinpath("l10n")


def get_l10n(locales=None, ftl_files=None):
    locales = locales or ["de", "en"]
    ftl_files = ftl_files or ["mozorg/fluent", "brands"]
    return fluent.fluent_l10n(locales, ftl_files)


@override_settings(FLUENT_PATHS=[L10N_PATH])
class TestFluentL10n(TestCase):
    def test_localized_bundles(self):
        l10n = get_l10n()
        bundles = list(l10n._bundles())
        localized_bundles = list(l10n._localized_bundles())
        assert len(bundles) == 2
        assert len(localized_bundles) == 1
        assert localized_bundles[0].locales[0] == "de"

    def test_localized_messages(self):
        l10n = get_l10n()
        assert len(l10n._localized_message_ids) == 4
        assert "brand-new-string" not in l10n._localized_message_ids

    def test_has_message(self):
        l10n = get_l10n()
        assert l10n.has_message("fluent-title")
        assert not l10n.has_message("brand-new-string")

    def test_required_messages(self):
        l10n = get_l10n()
        req_messages = l10n.required_message_ids
        assert "fluent-title" in req_messages
        assert "fluent-page-desc" in req_messages
        assert "fluent-header-title" not in req_messages
        assert "brand-new-string" not in req_messages

    def test_percent_translated(self):
        l10n = get_l10n()
        assert l10n.percent_translated == 80.0

    def test_has_required_messages(self):
        l10n = get_l10n()
        assert l10n.has_required_messages
        l10n = get_l10n(["fr", "en"])
        assert not l10n.has_required_messages


@override_settings(FLUENT_PATHS=[L10N_PATH], FLUENT_LOCAL_PATH=L10N_PATH)
class TestFluentTranslationUtils(TestCase):
    def setUp(self):
        fluent.cache.clear()

    def test_translate(self):
        l10n = get_l10n()
        assert fluent.translate(l10n, "fluent-title") == "Title in German"
        # does variable substition via kwargs
        assert fluent.translate(l10n, "fluent-page-desc", lang="Dudeish") == "Description in Dudeish"
        # fall back to 'en' string
        assert fluent.translate(l10n, "brand-new-string") == "New string not yet available in all languages"
        # will use fallback string
        assert fluent.translate(l10n, "brand-new-string", fallback="fluent-title") == "Title in German"

    def test_translate_term_fallback(self):
        """Test that translation will get the brand term from english"""
        # English works
        l10n = get_l10n(["en-US", "en"])
        assert fluent.translate(l10n, "fluent-brand") == "English Fluent"
        # German has no brands.ftl at all so falls back to English
        l10n = get_l10n(["de", "en"])
        assert fluent.translate(l10n, "fluent-brand") == "German Fluent"
        # French has a translation for the term
        l10n = get_l10n(["fr", "en"])
        assert fluent.translate(l10n, "fluent-brand") == "French Couramment"

    def test_has_all_messages(self):
        l10n = get_l10n()
        assert fluent.ftl_has_messages(l10n, "fluent-title", "fluent-page-desc")
        assert not fluent.ftl_has_messages(l10n, "fluent-title", "fluent-page-desc", "brand-new-string")

    def test_has_any_messages(self):
        l10n = get_l10n()
        assert fluent.ftl_has_messages(l10n, "fluent-title", "brand-new-string", require_all=False)
        assert not fluent.ftl_has_messages(l10n, "brand-new-string", require_all=False)

    @override_settings(DEV=True)
    @patch.object(fluent, "get_metadata")
    def test_get_active_locales(self, meta_mock):
        assert fluent.get_active_locales("the/dude") == settings.DEV_LANGUAGES
        meta_mock.assert_not_called()

        meta_mock.return_value = {
            "active_locales": ["de", "fr", "it"],
            "inactive_locales": ["it", "sq"],
        }
        assert fluent.get_active_locales("the/dude", force=True) == ["de", "en-US", "fr"]

    @override_settings(DEV=False)
    @patch.object(fluent, "get_metadata")
    def test_get_active_locales_multiple_files(self, meta_mock):
        meta_mock.side_effect = [
            {"active_locales": ["de", "fr", "it"]},
            {"active_locales": ["en-CA", "pt-BR", "it"]},
        ]
        assert fluent.get_active_locales(["the/dude", "the/walter"]) == [
            "de",
            "en-CA",
            "en-US",
            "fr",
            "it",
            "pt-BR",
        ]


@override_settings(FLUENT_PATHS=[L10N_PATH])
class TestFluentViewTranslationUtils(TestCase):
    def setUp(self):
        fluent.cache.clear()

    def test_ftl_view_util(self):
        assert fluent.ftl("fluent-title", locale="de", ftl_files="mozorg/fluent") == "Title in German"
        assert fluent.ftl("fluent-title", locale="fr", ftl_files="mozorg/fluent") == "Title in French"
        assert fluent.ftl("fluent-title", locale="en", ftl_files="mozorg/fluent") == "This is a test of the new Fluent L10n system"

    def test_ftl_view_util_no_mutate_list(self):
        """Should not mutate the ftl_files list"""
        ftl_files = ["mozorg/fluent"]
        assert fluent.ftl("fluent-title", locale="de", ftl_files=ftl_files) == "Title in German"
        assert ftl_files == ["mozorg/fluent"]

    def test_ftl_view_util_tuple(self):
        """Should be able to pass in a tuple of ftl files"""
        ftl_files = ("mozorg/fluent",)
        assert fluent.ftl("fluent-title", locale="de", ftl_files=ftl_files) == "Title in German"

    @override_settings(FLUENT_DEFAULT_FILES=["mozorg/fluent"])
    def test_ftl_view_util_default_files(self):
        """Should use default FTL files"""
        assert fluent.ftl("fluent-title", locale="de") == "Title in German"

    @override_settings(FLUENT_DEFAULT_FILES=["mozorg/fluent"])
    def test_ftl_view_util_active_locale(self):
        """Should use activated locale if not provided"""
        translation.activate("fr")
        assert fluent.ftl("fluent-title") == "Title in French"
