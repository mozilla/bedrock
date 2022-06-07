# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from pathlib import Path
from unittest.mock import patch

from django.http import Http404, HttpResponse
from django.test import RequestFactory, override_settings

from bedrock.legal_docs import views
from bedrock.legal_docs.models import LegalDoc, get_data_from_file_path
from bedrock.mozorg.tests import TestCase


@override_settings(PROD_LANGUAGES=["en-US", "de", "hi-IN"])
class TestLoadLegalDoc(TestCase):
    def test_legal_doc_not_found(self):
        """Missing doc should be None"""
        doc = views.load_legal_doc("the_dude_is_legal", "de")
        self.assertIsNone(doc)

    def test_legal_doc_exists(self):
        """Should return the content of the en-US file if it exists."""
        LegalDoc.objects.create(
            name="the_dude_exists",
            locale="en-US",
            content="You're not wrong Walter...",
        )
        doc = views.load_legal_doc("the_dude_exists", "de")
        self.assertEqual(doc["content"], "You're not wrong Walter...")
        self.assertEqual(doc["active_locales"], ["en-US"])

    @override_settings(IS_MOZORG_MODE=True)
    def test_legal_doc_exists_en_locale__mozorg_mode(self):
        """Should return the content of the "en" file and say the active locale is "en-US" if in Mozorg Mode"""
        LegalDoc.objects.create(
            name="the_dude_exists",
            locale="en",
            content="You're not wrong Walter...",
        )
        doc = views.load_legal_doc("the_dude_exists", "en-US")
        self.assertEqual(doc["content"], "You're not wrong Walter...")
        self.assertEqual(doc["active_locales"], ["en-US"])

    @override_settings(IS_MOZORG_MODE=False, PROD_LANGUAGES=["en", "de", "hi-IN"])
    def test_legal_doc_exists_en_locale__pocket_mode(self):
        """Should return the content of the "en" file and say the active locale is "en" if in Pocket Mode"""
        LegalDoc.objects.create(
            name="the_dude_exists",
            locale="en",
            content="You're not wrong Walter...",
        )
        doc = views.load_legal_doc("the_dude_exists", "en")
        self.assertEqual(doc["content"], "You're not wrong Walter...")
        self.assertEqual(doc["active_locales"], ["en"])

    def test_legal_doc_exists_snake_case_convert(self):
        """Should return the content of the file if it exists in snake case."""
        LegalDoc.objects.create(
            name="the_dude_exists",
            locale="en-US",
            content="You're not wrong Walter...",
        )
        doc = views.load_legal_doc("The-Dude-Exists", "de")
        self.assertEqual(doc["content"], "You're not wrong Walter...")
        self.assertEqual(doc["active_locales"], ["en-US"])

    def test_localized_legal_doc_exists(self):
        """Localization works, and list of translations doesn't include non .md files and non-prod locales."""
        LegalDoc.objects.create(
            name="the_dude_exists",
            locale="en",
            content="You're not wrong Walter...",
        )
        LegalDoc.objects.create(
            name="the_dude_exists",
            locale="de",
            content="You're in German Walter...",
        )
        doc = views.load_legal_doc("the_dude_exists", "de")
        self.assertEqual(doc["content"], "You're in German Walter...")
        self.assertEqual(set(doc["active_locales"]), {"de", "en-US"})


class TestLegalDocView(TestCase):
    @patch.object(views, "load_legal_doc")
    def test_missing_doc_is_404(self, lld_mock):
        lld_mock.return_value = None
        req = RequestFactory().get("/dude/is/gone/")
        req.locale = "de"
        view = views.LegalDocView.as_view(template_name="base.html", legal_doc_name="the_dude_is_gone")
        with self.assertRaises(Http404):
            view(req)

        lld_mock.assert_called_with("the_dude_is_gone", "de")

    @patch.object(views, "load_legal_doc")
    @patch.object(views.l10n_utils, "render")
    def test_good_doc_okay(self, render_mock, lld_mock):
        """Should render correct thing when all is well"""
        doc_value = "Donny, you're out of your element!"
        lld_mock.return_value = {
            "content": doc_value,
            "active_locales": ["de", "en-US"],
        }
        good_resp = HttpResponse(doc_value)
        render_mock.return_value = good_resp
        req = RequestFactory().get("/dude/exists/")
        req.locale = "de"
        view = views.LegalDocView.as_view(template_name="base.html", legal_doc_name="the_dude_exists")
        resp = view(req)
        assert resp["cache-control"] == f"max-age={views.CACHE_TIMEOUT!s}"
        assert resp.content.decode("utf-8") == doc_value
        assert render_mock.call_args[0][2]["doc"] == doc_value
        lld_mock.assert_called_with("the_dude_exists", "de")

    @patch.object(views, "load_legal_doc")
    @patch.object(views.l10n_utils, "render")
    def test_cache_settings(self, render_mock, lld_mock):
        """Should use the cache_timeout value from view."""
        doc_value = "Donny, you're out of your element!"
        lld_mock.return_value = {
            "content": doc_value,
            "active_locales": ["es-ES", "en-US"],
        }
        good_resp = HttpResponse(doc_value)
        render_mock.return_value = good_resp
        req = RequestFactory().get("/dude/exists/cached/")
        req.locale = "es-ES"
        view = views.LegalDocView.as_view(template_name="base.html", legal_doc_name="the_dude_exists", cache_timeout=10)
        resp = view(req)
        assert resp["cache-control"] == "max-age=10"

    @patch.object(views, "load_legal_doc")
    @patch.object(views.l10n_utils, "render")
    def test_cache_class_attrs(self, render_mock, lld_mock):
        """Should use the cache_timeout value from view class."""
        doc_value = "Donny, you're out of your element!"
        lld_mock.return_value = {
            "content": doc_value,
            "active_locales": ["es-ES", "en-US"],
        }
        good_resp = HttpResponse(doc_value)
        render_mock.return_value = good_resp
        req = RequestFactory().get("/dude/exists/cached/2/")
        req.locale = "es-ES"

        class DocTestView(views.LegalDocView):
            cache_timeout = 20
            template_name = "base.html"
            legal_doc_name = "the_dude_abides"

        view = DocTestView.as_view()
        resp = view(req)
        assert resp["cache-control"] == "max-age=20"
        lld_mock.assert_called_with("the_dude_abides", "es-ES")


class TestFilePathData(TestCase):
    def test_legacy_repo_layout(self):
        path = Path("/repo/data/legal_docs/websites_privacy_notice/en-US.md")
        assert get_data_from_file_path(path) == {
            "locale": "en-US",
            "doc_name": "websites_privacy_notice",
        }
        path = Path("/repo/data/legal_docs/websites_privacy_notice/de.md")
        assert get_data_from_file_path(path) == {
            "locale": "de",
            "doc_name": "websites_privacy_notice",
        }
        path = Path("/repo/data/legal_docs/firefox_privacy_notice/es-ES_b.md")
        assert get_data_from_file_path(path) == {
            "locale": "es-ES_b",
            "doc_name": "firefox_privacy_notice",
        }
        path = Path("/repo/data/legal_docs/WebRTC_ToS/cnh.md")
        assert get_data_from_file_path(path) == {
            "locale": "cnh",
            "doc_name": "WebRTC_ToS",
        }

    def test_new_repo_layout(self):
        path = Path("/repo/data/legal_docs/en-US/websites_privacy_notice.md")
        assert get_data_from_file_path(path) == {
            "locale": "en-US",
            "doc_name": "websites_privacy_notice",
        }
        path = Path("/repo/data/legal_docs/de/websites_privacy_notice.md")
        assert get_data_from_file_path(path) == {
            "locale": "de",
            "doc_name": "websites_privacy_notice",
        }
        path = Path("/repo/data/legal_docs/es-ES_b/firefox_privacy_notice.md")
        assert get_data_from_file_path(path) == {
            "locale": "es-ES_b",
            "doc_name": "firefox_privacy_notice",
        }
        path = Path("/repo/data/legal_docs/cnh/WebRTC_ToS.md")
        assert get_data_from_file_path(path) == {
            "locale": "cnh",
            "doc_name": "WebRTC_ToS",
        }
