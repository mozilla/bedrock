# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import patch

from django.http import Http404, HttpResponse
from django.test.client import RequestFactory

from bs4 import BeautifulSoup
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


class TestProcessLegalDoc(TestCase):
    def hrefs(self, html):
        return [link["href"] for link in views.process_legal_doc(html).find_all("a")]

    def test_returns_a_soup_object(self):
        doc = views.process_legal_doc("<p>Legalese</p>")
        assert isinstance(doc, BeautifulSoup)
        assert doc.find("p").text == "Legalese"

    def test_secure_mozorg_links_become_paths(self):
        assert self.hrefs('<a href="https://www.mozilla.org/en-US/about/">About</a>') == ["/en-US/about/"]

    def test_insecure_mozorg_links_become_paths(self):
        assert self.hrefs('<a href="http://www.mozilla.org/en-US/about/">About</a>') == ["/en-US/about/"]

    def test_external_links_are_untouched(self):
        assert self.hrefs('<a href="https://example.com/en-US/about/">About</a>') == ["https://example.com/en-US/about/"]

    def test_relative_links_are_untouched(self):
        assert self.hrefs('<a href="/en-US/privacy/">Privacy</a>') == ["/en-US/privacy/"]

    def test_only_the_start_of_an_href_is_matched(self):
        # HREF_PATTERN is anchored, so a mozilla.org URL further into the href stays put
        href = "https://example.com/redirect?to=https://www.mozilla.org/en-US/"
        assert self.hrefs(f'<a href="{href}">Redirect</a>') == [href]

    def test_every_matching_link_is_rewritten(self):
        html = (
            '<a href="https://www.mozilla.org/en-US/about/">About</a>'
            '<a href="https://www.mozilla.org/en-US/contact/">Contact</a>'
            '<a href="https://example.com/">Example</a>'
        )
        assert self.hrefs(html) == ["/en-US/about/", "/en-US/contact/", "https://example.com/"]

    def test_rewrite_is_not_limited_to_anchors(self):
        # find_all(href=...) matches any tag carrying an href, not just <a>
        doc = views.process_legal_doc('<link href="https://www.mozilla.org/style.css">')
        assert doc.find("link")["href"] == "/style.css"

    def test_doc_without_links_is_returned_unchanged(self):
        doc = views.process_legal_doc("<h1>Privacy Notice</h1><p>No links here.</p>")
        assert doc.find("h1").text == "Privacy Notice"
        assert doc.find_all("a") == []


class TestPrivacyDocView(TestCase):
    def get_legal_doc(self, doc):
        with patch("bedrock.legal_docs.views.load_legal_doc", return_value=doc):
            view = views.PrivacyDocView()
            view.request = RequestFactory().get("/en-US/privacy/websites/")
            return view.get_legal_doc()

    def test_content_is_processed(self):
        doc = self.get_legal_doc(
            {
                "content": '<a href="https://www.mozilla.org/en-US/about/">About</a>',
                "active_locales": ["de", "en-US"],
            }
        )
        assert isinstance(doc["content"], BeautifulSoup)
        assert doc["content"].find("a")["href"] == "/en-US/about/"

    def test_active_locales_are_left_alone(self):
        doc = self.get_legal_doc({"content": "<p>Legalese</p>", "active_locales": ["de", "en-US"]})
        assert doc["active_locales"] == ["de", "en-US"]

    def test_missing_doc_is_passed_through(self):
        assert self.get_legal_doc(None) is None

    def test_missing_doc_gives_404(self):
        with patch("bedrock.legal_docs.views.load_legal_doc", return_value=None):
            view = views.PrivacyDocView()
            view.request = RequestFactory().get("/en-US/privacy/websites/")
            with self.assertRaises(Http404):
                view.get_context_data()


class TestFirefoxPrivacyPreviewTemplates(TestCase):
    @patch.object(views.PrivacyDocView, "get_legal_doc")
    @patch("bedrock.privacy.views.l10n_utils.render", return_value=HttpResponse())
    def test_simple_template(self, render_mock, lld_mock):
        with override_switch("ENABLE_FIREFOX_PRIVACY_NEXT", active=True):
            lld_mock.return_value["content"].select.return_value = None
            resp = self.client.get("/en-US/privacy/firefox/next/?v=product")
            assert resp.status_code == 200
            assert render_mock.call_args[0][1] == "privacy/notices/firefox-simple.html"


class TestPrivacyIndexView(TestCase):
    @patch("bedrock.privacy.views.l10n_utils.render", return_value=HttpResponse())
    @patch("bedrock.privacy.views.load_legal_doc")
    def test_renders_processed_doc(self, load_mock, render_mock):
        load_mock.return_value = {
            "content": '<a href="https://www.mozilla.org/en-US/about/">About</a>',
            "active_locales": ["de", "en-US"],
        }
        req = RequestFactory().get("/en-US/privacy/")
        req.locale = "en-US"
        views.privacy(req)

        load_mock.assert_called_once_with("mozilla_privacy_policy", "en-US")
        args, kwargs = render_mock.call_args
        assert args[1] == "privacy/index.html"
        assert args[2]["doc"].find("a")["href"] == "/en-US/about/"
        assert args[2]["active_locales"] == ["de", "en-US"]
        assert kwargs["ftl_files"] == "privacy/index"

    @patch("bedrock.privacy.views.l10n_utils.render", return_value=HttpResponse())
    @patch("bedrock.privacy.views.load_legal_doc")
    def test_doc_is_loaded_for_the_request_locale(self, load_mock, render_mock):
        load_mock.return_value = {"content": "<p>Legalese</p>", "active_locales": ["de"]}
        req = RequestFactory().get("/de/privacy/")
        req.locale = "de"
        views.privacy(req)

        load_mock.assert_called_once_with("mozilla_privacy_policy", "de")

    @patch("bedrock.privacy.views.load_legal_doc", return_value=None)
    def test_missing_doc_gives_404(self, load_mock):
        req = RequestFactory().get("/en-US/privacy/")
        req.locale = "en-US"
        with self.assertRaises(Http404):
            views.privacy(req)


class TestPrivacyFAQView(TestCase):
    @patch("bedrock.privacy.views.ftl_file_is_active", return_value=True)
    def test_v2_template_when_ftl_file_is_active(self, ftl_mock):
        assert views.FAQView().get_template_names() == ["privacy/faq-v2.html"]
        ftl_mock.assert_called_once_with("privacy/faq-v2")

    @patch("bedrock.privacy.views.ftl_file_is_active", return_value=False)
    def test_legacy_template_when_ftl_file_is_inactive(self, ftl_mock):
        assert views.FAQView().get_template_names() == ["privacy/faq.html"]
