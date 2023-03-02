# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# coding: utf-8

import os.path
from datetime import datetime
from unittest.mock import patch

from django.conf import settings
from django.test.client import RequestFactory
from django.test.utils import override_settings

import pytest
from bs4 import BeautifulSoup
from django_jinja.backend import Jinja2
from markupsafe import Markup
from pyquery import PyQuery as pq

from bedrock.base.templatetags.helpers import static
from bedrock.mozorg.templatetags import misc
from bedrock.mozorg.tests import TestCase
from lib.l10n_utils.fluent import fluent_l10n

TEST_FILES_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_files")
TEST_L10N_MEDIA_PATH = os.path.join(TEST_FILES_ROOT, "media", "%s", "l10n")

TEST_FXA_ENDPOINT = "https://accounts.firefox.com/"

jinja_env = Jinja2.get_default()


# Where should this function go?
def render(s, context=None):
    t = jinja_env.from_string(s)
    return t.render(context or {})


def test_convert_to_high_res():
    assert misc.convert_to_high_res("/media/img/the.dude.png") == "/media/img/the.dude-high-res.png"
    assert misc.convert_to_high_res("/media/thats-a-bummer-man.jpg") == "/media/thats-a-bummer-man-high-res.jpg"


@patch("bedrock.mozorg.templatetags.misc._l10n_media_exists")
@patch("django.conf.settings.LANGUAGE_CODE", "en-US")
class TestImgL10n(TestCase):
    rf = RequestFactory()

    def _render(self, locale, url):
        req = self.rf.get("/")
        req.locale = locale
        return render(f"{{{{ l10n_img('{url}') }}}}", {"request": req})

    def test_works_for_default_lang(self, media_exists_mock):
        """Should output correct path for default lang always."""
        media_exists_mock.return_value = True
        assert self._render("en-US", "dino/head.png") == static("img/l10n/en-US/dino/head.png")
        assert self._render("en-US", "img/dino/head.png") == static("img/l10n/en-US/dino/head.png")

        assert self._render("en-US", "dino/does-not-exist.png") == static("img/l10n/en-US/dino/does-not-exist.png")

    def test_works_for_other_lang(self, media_exists_mock):
        """Should use the request lang if file exists."""
        media_exists_mock.return_value = True
        assert self._render("de", "dino/head.png") == static("img/l10n/de/dino/head.png")
        assert self._render("de", "img/dino/head.png") == static("img/l10n/de/dino/head.png")

    def test_defaults_when_lang_file_missing(self, media_exists_mock):
        """Should use default lang when file doesn't exist for lang."""
        media_exists_mock.return_value = False
        assert self._render("is", "dino/head.png") == static("img/l10n/en-US/dino/head.png")

    def test_latam_spanishes_fallback_to_european_spanish(self, media_exists_mock):
        """Should use es-ES image when file doesn't exist for lang."""
        media_exists_mock.side_effect = [False, True]
        assert self._render("es-AR", "dino/head.png") == static("img/l10n/es-ES/dino/head.png")

        media_exists_mock.reset_mock()
        media_exists_mock.side_effect = [False, True]
        assert self._render("es-CL", "dino/head.png") == static("img/l10n/es-ES/dino/head.png")

        media_exists_mock.reset_mock()
        media_exists_mock.side_effect = [False, True]
        assert self._render("es-MX", "dino/head.png") == static("img/l10n/es-ES/dino/head.png")

        media_exists_mock.reset_mock()
        media_exists_mock.side_effect = [False, True]
        assert self._render("es", "dino/head.png") == static("img/l10n/es-ES/dino/head.png")

    def test_file_not_checked_for_default_lang(self, media_exists_mock):
        """
        Should not check filesystem for default lang, but should for others.
        """
        assert self._render("en-US", "dino/does-not-exist.png") == static("img/l10n/en-US/dino/does-not-exist.png")
        assert not media_exists_mock.called

        self._render("is", "dino/does-not-exist.png")
        media_exists_mock.assert_called_once_with("img", "is", "dino/does-not-exist.png")


@override_settings(DEBUG=False)
@patch("bedrock.mozorg.templatetags.misc._l10n_media_exists")
class TestL10nCSS(TestCase):
    rf = RequestFactory()
    static_url_dev = "/static/"
    cdn_url = "//mozorg.cdn.mozilla.net"
    static_url_prod = cdn_url + static_url_dev
    markup = '<link rel="stylesheet" media="screen,projection,tv" href=' '"%scss/l10n/%s/intl.css">'

    def _render(self, locale):
        req = self.rf.get("/")
        req.locale = locale
        return render("{{ l10n_css() }}", {"request": req})

    @override_settings(DEV=True)
    @patch("django.contrib.staticfiles.storage.staticfiles_storage.base_url", static_url_dev)
    def test_dev_when_css_file_exists(self, media_exists_mock):
        """Should output a path to the CSS file if exists."""
        media_exists_mock.return_value = True
        assert self._render("de") == self.markup % (self.static_url_dev, "de")
        assert self._render("es-ES") == self.markup % (self.static_url_dev, "es-ES")

    @override_settings(DEV=True)
    def test_dev_when_css_file_missing(self, media_exists_mock):
        """Should output nothing if the CSS file is missing."""
        media_exists_mock.return_value = False
        assert self._render("en-US") == ""
        assert self._render("fr") == ""

    @override_settings(DEV=False)
    @patch("django.contrib.staticfiles.storage.staticfiles_storage.base_url", static_url_prod)
    def test_prod_when_css_file_exists(self, media_exists_mock):
        """Should output a path to the CSS file if exists."""
        media_exists_mock.return_value = True
        assert self._render("de") == self.markup % (self.static_url_prod, "de")
        assert self._render("es-ES") == self.markup % (self.static_url_prod, "es-ES")

    @override_settings(DEV=False)
    def test_prod_when_css_file_missing(self, media_exists_mock):
        """Should output nothing if the CSS file is missing."""
        media_exists_mock.return_value = False
        assert self._render("en-US") == ""
        assert self._render("fr") == ""


class TestVideoTag(TestCase):
    rf = RequestFactory()
    # Video stubs
    moz_video = "http://videos.mozilla.org/serv/flux/example.%s"
    nomoz_video = "http://example.org/example.%s"

    def get_l10n(self, locale):
        return fluent_l10n([locale, "en"], settings.FLUENT_DEFAULT_FILES)

    def _render(self, template):
        req = self.rf.get("/")
        req.locale = "en-US"
        return render(template, {"request": req, "fluent_l10n": self.get_l10n(req.locale)})

    def test_empty(self):
        # No video, no output.
        assert render("{{ video() }}") == ""
        assert render("{{ video('missing-ext') }}") == ""

    def test_video(self):
        # A few common variations
        videos = [self.nomoz_video % ext for ext in ("ogv", "mp4", "webm")]
        doc = pq(self._render("{{ video%s }}" % str(tuple(videos))))

        # Tags generated?
        assert doc("video").length == 1
        assert doc("video source").length == 3

        # Extensions in the right order?
        extensions = [os.path.splitext(el.attrib["src"])[1] for el in doc("video source")]
        assert extensions == [".webm", ".ogv", ".mp4"]

    def test_prefix(self):
        # Prefix should be applied to all videos.
        doc = pq(self._render("{{ video('meh.mp4', 'meh.ogv', prefix='http://example.com/blah/') }}"))
        assert [el.attrib["src"] for el in doc("video source")] == [
            "http://example.com/blah/meh.ogv",
            "http://example.com/blah/meh.mp4",
        ]

    def test_fileformats(self):
        # URLs ending in strange extensions are ignored.
        videos = [self.nomoz_video % ext for ext in ("ogv", "exe", "webm", "txt")]
        videos.append("http://example.net/noextension")
        doc = pq(self._render("{{ video%s }}" % (str(tuple(videos)))))

        assert doc("video source").length == 2

        extensions = [os.path.splitext(el.attrib["src"])[1] for el in doc("video source")]
        assert extensions == [".webm", ".ogv"]


@override_settings(STATIC_URL="/media/")
@patch("bedrock.mozorg.templatetags.misc.find_static", return_value=True)
class TestPlatformImg(TestCase):
    rf = RequestFactory()

    def _render(self, url, optional_attributes=None):
        req = self.rf.get("/")
        req.locale = "en-US"
        return render(f"{{{{ platform_img('{url}', {optional_attributes}) }}}}", {"request": req})

    def _render_l10n(self, url):
        req = self.rf.get("/")
        req.locale = "en-US"
        return render(f"{{{{ l10n_img('{url}') }}}}", {"request": req})

    def test_platform_img_no_optional_attributes(self, find_static):
        """Should return expected markup without optional attributes"""
        markup = self._render("test.png")
        self.assertIn('data-src-windows="/media/test-windows.png"', markup)
        self.assertIn('data-src-mac="/media/test-mac.png"', markup)
        markup = self._render("img/test.png")
        self.assertIn('data-src-windows="/media/img/test-windows.png"', markup)
        self.assertIn('data-src-mac="/media/img/test-mac.png"', markup)

    def test_platform_img_with_optional_attributes(self, find_static):
        """Should return expected markup with optional attributes"""
        markup = self._render("test.png", {"data-test-attr": "test"})
        self.assertIn('data-test-attr="test"', markup)

    def test_platform_img_with_high_res(self, find_static):
        """Should return expected markup with high resolution image attrs"""
        markup = self._render("test.png", {"high-res": True})
        self.assertIn('data-src-windows-high-res="/media/test-windows-high-res.png"', markup)
        self.assertIn('data-src-mac-high-res="/media/test-mac-high-res.png"', markup)
        self.assertIn('data-high-res="true"', markup)
        markup = self._render("img/test.png", {"high-res": True})
        self.assertIn('data-src-windows-high-res="/media/img/test-windows-high-res.png"', markup)
        self.assertIn('data-src-mac-high-res="/media/img/test-mac-high-res.png"', markup)
        self.assertIn('data-high-res="true"', markup)

    def test_platform_img_with_l10n(self, find_static):
        """Should return expected markup with l10n image path"""
        l10n_url_win = self._render_l10n("test-windows.png")
        l10n_url_mac = self._render_l10n("test-mac.png")
        markup = self._render("test.png", {"l10n": True})
        self.assertIn('data-src-windows="' + l10n_url_win + '"', markup)
        self.assertIn('data-src-mac="' + l10n_url_mac + '"', markup)
        markup = self._render("/img/test.png", {"l10n": True})
        self.assertIn('data-src-windows="' + l10n_url_win + '"', markup)
        self.assertIn('data-src-mac="' + l10n_url_mac + '"', markup)

    def test_platform_img_with_l10n_and_optional_attributes(self, find_static):
        """
        Should return expected markup with l10n image path and optional
        attributes
        """
        l10n_url_win = self._render_l10n("test-windows.png")
        l10n_url_mac = self._render_l10n("test-mac.png")
        markup = self._render("test.png", {"l10n": True, "data-test-attr": "test"})
        self.assertIn('data-src-windows="' + l10n_url_win + '"', markup)
        self.assertIn('data-src-mac="' + l10n_url_mac + '"', markup)
        self.assertIn('data-test-attr="test"', markup)

    def test_platform_img_with_l10n_and_high_res(self, find_static):
        """
        Should return expected markup with l10n image path and high resolution
        attributes
        """
        l10n_url_win = self._render_l10n("test-windows.png")
        l10n_hr_url_win = misc.convert_to_high_res(l10n_url_win)
        l10n_url_mac = self._render_l10n("test-mac.png")
        l10n_hr_url_mac = misc.convert_to_high_res(l10n_url_mac)
        markup = self._render("test.png", {"l10n": True, "high-res": True})
        self.assertIn('data-src-windows-high-res="' + l10n_hr_url_win + '"', markup)
        self.assertIn('data-src-mac-high-res="' + l10n_hr_url_mac + '"', markup)
        self.assertIn('data-high-res="true"', markup)


class TestPressBlogUrl(TestCase):
    rf = RequestFactory()

    def _render(self, locale):
        req = self.rf.get("/")
        req.locale = locale
        return render("{{{{ press_blog_url() }}}}".format("/"), {"request": req})  # noqa: F523

    def test_press_blog_url_no_locale(self):
        """No locale, fallback to default press blog"""
        assert self._render("") == "https://blog.mozilla.org/press/"

    def test_press_blog_url_english(self):
        """en-US locale, default press blog"""
        assert self._render("en-US") == "https://blog.mozilla.org/press/"

    def test_press_blog_url_europe(self):
        """Major European locales have their own blog"""
        assert self._render("es-ES") == "https://blog.mozilla.org/press-es/"
        assert self._render("fr") == "https://blog.mozilla.org/press-fr/"
        assert self._render("de") == "https://blog.mozilla.org/press-de/"
        assert self._render("pl") == "https://blog.mozilla.org/press-pl/"
        assert self._render("it") == "https://blog.mozilla.org/press-it/"
        assert self._render("en-GB") == "https://blog.mozilla.org/press-uk/"

    def test_press_blog_url_latam(self):
        """South American Spanishes use the es-ES blog"""
        assert self._render("es-AR") == "https://blog.mozilla.org/press-es/"
        assert self._render("es-CL") == "https://blog.mozilla.org/press-es/"
        assert self._render("es-MX") == "https://blog.mozilla.org/press-es/"

    def test_press_blog_url_brazil(self):
        """Brazilian Portuguese has its own br blog"""
        assert self._render("pt-BR") == "https://blog.mozilla.org/press-br/"

    def test_press_blog_url_other_locale(self):
        """No blog for locale, fallback to default press blog"""
        assert self._render("oc") == "https://blog.mozilla.org/press/"


class TestDonateUrl(TestCase):
    rf = RequestFactory()

    def _render(self, content=""):
        req = self.rf.get("/")
        return render(f"{{{{ donate_url(content='{content}') }}}}", {"request": req})

    def test_donate_url_with_content_param(self):
        """Should include campaign specific parameters when supplied"""
        assert self._render(content="footer") == (
            "https://foundation.mozilla.org/?form=donate&amp;c_id=7014x000000eQOH&amp;utm_source=mozilla.org&amp;utm_medium=referral"
            "&amp;utm_campaign=moco&amp;utm_content=footer"
        )

    def test_donate_url_no_params(self):
        """Should exclude campaign specific parameters when not supplied"""
        assert self._render() == (
            "https://foundation.mozilla.org/?form=donate&amp;c_id=7014x000000eQOH&amp;utm_source=mozilla.org&amp;utm_medium=referral"
            "&amp;utm_campaign=moco"
        )


class TestFirefoxTwitterUrl(TestCase):
    rf = RequestFactory()

    def _render(self, locale):
        req = self.rf.get("/")
        req.locale = locale
        return render("{{ firefox_twitter_url() }}", {"request": req})

    def test_firefox_twitter_url_no_locale(self):
        """No locale, fallback to default account"""
        assert self._render("") == "https://twitter.com/firefox"

    def test_firefox_twitter_url_english(self):
        """en-US locale, default account"""
        assert self._render("en-US") == "https://twitter.com/firefox"

    def test_firefox_twitter_url_spanish(self):
        """es-ES locale, a local account"""
        assert self._render("es-ES") == "https://twitter.com/firefox_es"

    def test_firefox_twitter_url_portuguese(self):
        """pt-BR locale, a local account"""
        assert self._render("pt-BR") == "https://twitter.com/firefoxbrasil"

    def test_firefox_twitter_url_other_locale(self):
        """No account for locale, fallback to default account"""
        assert self._render("es-AR") == "https://twitter.com/firefox"
        assert self._render("es-CL") == "https://twitter.com/firefox"
        assert self._render("es-MX") == "https://twitter.com/firefox"
        assert self._render("pt-PT") == "https://twitter.com/firefox"


class TestMozillaTwitterUrl(TestCase):
    rf = RequestFactory()

    def _render(self, locale):
        req = self.rf.get("/")
        req.locale = locale
        return render("{{ mozilla_twitter_url() }}", {"request": req})

    def test_mozilla_twitter_url_no_locale(self):
        """No locale, fallback to default account"""
        assert self._render("") == "https://twitter.com/mozilla"

    def test_mozilla_twitter_url_english(self):
        """en-US locale, default account"""
        assert self._render("en-US") == "https://twitter.com/mozilla"

    def test_mozilla_twitter_url_french(self):
        """fr locale, a local account"""
        assert self._render("fr") == "https://twitter.com/mozilla_france"

    def test_mozilla_twitter_url_german(self):
        """de locale, a local account"""
        assert self._render("de") == "https://twitter.com/mozilla_germany"

    def test_mozilla_twitter_url_other_locale(self):
        """No account for locale, fallback to default account"""
        assert self._render("es-AR") == "https://twitter.com/mozilla"
        assert self._render("es-CL") == "https://twitter.com/mozilla"
        assert self._render("es-MX") == "https://twitter.com/mozilla"
        assert self._render("pt-PT") == "https://twitter.com/mozilla"


class TestMozillaInstagramUrl(TestCase):
    rf = RequestFactory()

    def _render(self, locale):
        req = self.rf.get("/")
        req.locale = locale
        return render("{{ mozilla_instagram_url() }}", {"request": req})

    def test_mozilla_instagram_url_no_locale(self):
        """No locale, fallback to default account"""
        assert self._render("") == "https://www.instagram.com/mozilla/"

    def test_mozilla_instagram_url_english(self):
        """en-US locale, default account"""
        assert self._render("en-US") == "https://www.instagram.com/mozilla/"

    def test_mozilla_instagram_url_german(self):
        """de locale, a local account"""
        assert self._render("de") == "https://www.instagram.com/mozilla_deutschland/"

    def test_mozilla_instagram_url_other_locale(self):
        """No account for locale, fallback to default account"""
        assert self._render("es-AR") == "https://www.instagram.com/mozilla/"


@override_settings(STATIC_URL="/media/")
class TestHighResImg(TestCase):
    rf = RequestFactory()

    def _render(self, url, optional_attributes=None):
        req = self.rf.get("/")
        req.locale = "en-US"
        return render(f"{{{{ high_res_img('{url}', {optional_attributes}) }}}}", {"request": req})

    def _render_l10n(self, url):
        req = self.rf.get("/")
        req.locale = "en-US"
        return render(f"{{{{ l10n_img('{url}') }}}}", {"request": req})

    def test_high_res_img_no_optional_attributes(self):
        """Should return expected markup without optional attributes"""
        expected = '<img class="" src="/media/img/test.png" ' 'srcset="/media/img/test-high-res.png 1.5x">'
        markup = self._render("img/test.png")
        self.assertEqual(markup, expected)

    def test_high_res_img_with_optional_attributes(self):
        """Should return expected markup with optional attributes"""
        markup = self._render("img/test.png", {"data-test-attr": "test", "class": "logo"})
        expected = '<img class="logo" src="/media/img/test.png" ' 'srcset="/media/img/test-high-res.png 1.5x" ' 'data-test-attr="test">'
        self.assertEqual(markup, expected)

    def test_high_res_img_with_l10n(self):
        """Should return expected markup with l10n image path"""
        l10n_url = self._render_l10n("test.png")
        l10n_hr_url = misc.convert_to_high_res(l10n_url)
        markup = self._render("test.png", {"l10n": True})
        expected = '<img class="" src="' + l10n_url + '" ' 'srcset="' + l10n_hr_url + ' 1.5x">'
        self.assertEqual(markup, expected)

        l10n_url = self._render_l10n("img/test.png")
        l10n_hr_url = misc.convert_to_high_res(l10n_url)
        markup = self._render("test.png", {"l10n": True})
        expected = '<img class="" src="' + l10n_url + '" ' 'srcset="' + l10n_hr_url + ' 1.5x">'
        self.assertEqual(markup, expected)

    def test_high_res_img_with_l10n_and_optional_attributes(self):
        """Should return expected markup with l10n image path"""
        l10n_url = self._render_l10n("test.png")
        l10n_hr_url = misc.convert_to_high_res(l10n_url)
        markup = self._render("test.png", {"l10n": True, "data-test-attr": "test"})
        expected = '<img class="" src="' + l10n_url + '" ' 'srcset="' + l10n_hr_url + ' 1.5x" data-test-attr="test">'
        self.assertEqual(markup, expected)


@override_settings(STATIC_URL="/media/")
class TestRespImg(TestCase):
    rf = RequestFactory()

    def _render(self, url, srcset=None, sizes=None, optional_attributes=None):
        req = self.rf.get("/")
        req.locale = "en-US"
        return render(f"{{{{ resp_img('{url}', {srcset}, {sizes}, {optional_attributes}) }}}}", {"request": req})

    def _render_l10n(self, url):
        req = self.rf.get("/")
        req.locale = "en-US"
        return render(f"{{{{ l10n_img('{url}') }}}}", {"request": req})

    def test_resp_img_no_optional_attributes(self):
        """Should return expected markup without optional attributes"""
        expected = (
            '<img src="/media/img/panda-500.png" '
            'srcset="/media/img/panda-500.png 500w,/media/img/panda-1000.png 1000w" '
            'sizes="(min-width: 1000px) calc(50vw - 200px),calc(100vw - 50px)" alt="">'
        )
        markup = self._render(
            "img/panda-500.png",
            {"img/panda-500.png": "500w", "img/panda-1000.png": "1000w"},
            {"(min-width: 1000px)": "calc(50vw - 200px)", "default": "calc(100vw - 50px)"},
        )
        self.assertEqual(markup, expected)

    def test_resp_img_absolute_urls(self):
        """Should return expected markup when absolute image URLs are passed"""
        expected = (
            '<img src="https://www.example.com/img/panda-500.png" '
            'srcset="https://www.example.com/img/panda-500.png 500w,https://www.example.com/img/panda-1000.png 1000w" '
            'sizes="(min-width: 1000px) calc(50vw - 200px),calc(100vw - 50px)" alt="">'
        )
        markup = self._render(
            "https://www.example.com/img/panda-500.png",
            {"https://www.example.com/img/panda-500.png": "500w", "https://www.example.com/img/panda-1000.png": "1000w"},
            {"(min-width: 1000px)": "calc(50vw - 200px)", "default": "calc(100vw - 50px)"},
        )
        self.assertEqual(markup, expected)

    def test_resp_img_with_optional_attributes(self):
        """Should return expected markup with optional attributes"""
        expected = (
            '<img src="/media/img/panda-500.png" '
            'srcset="/media/img/panda-500.png 500w,/media/img/panda-1000.png 1000w" '
            'sizes="(min-width: 1000px) calc(50vw - 200px),calc(100vw - 50px)" '
            'alt="Red Panda" class="panda-hero" loading="lazy">'
        )
        markup = self._render(
            "img/panda-500.png",
            {"img/panda-500.png": "500w", "img/panda-1000.png": "1000w"},
            {"(min-width: 1000px)": "calc(50vw - 200px)", "default": "calc(100vw - 50px)"},
            {"class": "panda-hero", "alt": "Red Panda", "loading": "lazy"},
        )
        self.assertEqual(markup, expected)

    def test_resp_img_with_l10n(self):
        """Should return expected markup with l10n image path"""
        expected = (
            '<img src="/media/img/l10n/en-US/panda-500.png" '
            'srcset="/media/img/l10n/en-US/panda-500.png 500w,/media/img/l10n/en-US/panda-1000.png 1000w" '
            'sizes="(min-width: 1000px) calc(50vw - 200px),calc(100vw - 50px)" alt="">'
        )
        markup = self._render(
            "panda-500.png",
            {"panda-500.png": "500w", "panda-1000.png": "1000w"},
            {"(min-width: 1000px)": "calc(50vw - 200px)", "default": "calc(100vw - 50px)"},
            {"l10n": True},
        )
        self.assertEqual(markup, expected)

        expected = (
            '<img src="/media/img/l10n/en-US/panda-500.png" '
            'srcset="/media/img/l10n/en-US/panda-500.png 500w,/media/img/l10n/en-US/panda-1000.png 1000w" '
            'sizes="(min-width: 1000px) calc(50vw - 200px),calc(100vw - 50px)" alt="">'
        )
        markup = self._render(
            "img/panda-500.png",
            {"img/panda-500.png": "500w", "img/panda-1000.png": "1000w"},
            {"(min-width: 1000px)": "calc(50vw - 200px)", "default": "calc(100vw - 50px)"},
            {"l10n": True},
        )
        self.assertEqual(markup, expected)

    def test_resp_img_with_l10n_and_optional_attributes(self):
        """Should return expected markup with l10n image path"""
        expected = (
            '<img src="/media/img/l10n/en-US/panda-500.png" '
            'srcset="/media/img/l10n/en-US/panda-500.png 500w,/media/img/l10n/en-US/panda-1000.png 1000w" '
            'sizes="(min-width: 1000px) calc(50vw - 200px),calc(100vw - 50px)" '
            'alt="Red Panda" class="panda-hero" loading="lazy">'
        )
        markup = self._render(
            "img/panda-500.png",
            {"img/panda-500.png": "500w", "img/panda-1000.png": "1000w"},
            {"(min-width: 1000px)": "calc(50vw - 200px)", "default": "calc(100vw - 50px)"},
            {"l10n": True, "class": "panda-hero", "alt": "Red Panda", "loading": "lazy"},
        )
        self.assertEqual(markup, expected)

    def test_resp_img_srcset_without_sizes(self):
        """Should return expected markup when using srcset without sizes"""
        expected = '<img src="/media/img/panda.png" srcset="/media/img/panda-high-res.png 2x" alt="">'
        markup = self._render("img/panda.png", {"img/panda-high-res.png": "2x"})
        self.assertEqual(markup, expected)

    def test_resp_img_without_srcset_or_sizes(self):
        """Should return expected markup when using without srcset or sizes"""
        expected = '<img src="/media/img/panda.png" alt="">'
        markup = self._render("img/panda.png")
        self.assertEqual(markup, expected)


@override_settings(STATIC_URL="/media/")
class TestPicture(TestCase):
    rf = RequestFactory()

    def _render(self, url, sources, optional_attributes=None):
        req = self.rf.get("/")
        req.locale = "en-US"
        return render(f"{{{{ picture('{url}', {sources}, {optional_attributes}) }}}}", {"request": req})

    def test_picture_media_srcset_only(self):
        """Should return expected markup when specifying media and srcset"""
        expected = (
            "<picture>"
            '<source media="(max-width: 799px)" srcset="/media/img/panda-mobile.png">'
            '<source media="(min-width: 800px)" srcset="/media/img/panda-desktop.png">'
            '<img src="/media/img/panda-mobile.png" alt="">'
            "</picture>"
        )
        markup = self._render(
            "img/panda-mobile.png",
            [
                {"media": "(max-width: 799px)", "srcset": {"img/panda-mobile.png": "default"}},
                {"media": "(min-width: 800px)", "srcset": {"img/panda-desktop.png": "default"}},
            ],
        )
        self.assertEqual(markup, expected)

    def test_picture_absolute_urls(self):
        """Should return expected markup when absolute image urls are passed"""
        expected = (
            "<picture>"
            '<source media="(max-width: 799px)" srcset="https://www.example.com/img/panda-mobile.png">'
            '<source media="(min-width: 800px)" srcset="https://www.example.com/img/panda-desktop.png">'
            '<img src="https://www.example.com/img/panda-mobile.png" alt="">'
            "</picture>"
        )
        markup = self._render(
            "https://www.example.com/img/panda-mobile.png",
            [
                {"media": "(max-width: 799px)", "srcset": {"https://www.example.com/img/panda-mobile.png": "default"}},
                {"media": "(min-width: 800px)", "srcset": {"https://www.example.com/img/panda-desktop.png": "default"}},
            ],
        )
        self.assertEqual(markup, expected)

    def test_picture_media_multiple_srcset_sizes(self):
        """Should return expected markup when specifying media with multiple srcset and sizes"""
        expected = (
            "<picture>"
            '<source media="(prefers-reduced-motion: reduce)" '
            'srcset="/media/img/sleeping-panda-500.png 500w,/media/img/sleeping-panda-1000.png 1000w" '
            'sizes="(min-width: 1000px) calc(50vw - 200px),calc(100vw - 50px)">'
            '<source media="(prefers-reduced-motion: no-preference)" '
            'srcset="/media/img/dancing-panda-500.gif 500w,/media/img/dancing-panda-1000.gif 1000w" '
            'sizes="(min-width: 1000px) calc(50vw - 200px),calc(100vw - 50px)">'
            '<img src="/media/img/dancing-panda-500.gif" alt="">'
            "</picture>"
        )
        markup = self._render(
            "img/dancing-panda-500.gif",
            [
                {
                    "media": "(prefers-reduced-motion: reduce)",
                    "srcset": {"img/sleeping-panda-500.png": "500w", "img/sleeping-panda-1000.png": "1000w"},
                    "sizes": {"(min-width: 1000px)": "calc(50vw - 200px)", "default": "calc(100vw - 50px)"},
                },
                {
                    "media": "(prefers-reduced-motion: no-preference)",
                    "srcset": {"img/dancing-panda-500.gif": "500w", "img/dancing-panda-1000.gif": "1000w"},
                    "sizes": {"(min-width: 1000px)": "calc(50vw - 200px)", "default": "calc(100vw - 50px)"},
                },
            ],
        )
        self.assertEqual(markup, expected)

    def test_picture_type_srcset_only(self):
        """Should return expected markup when specifying type and srcset"""
        expected = '<picture><source type="image/webp" srcset="/media/img/red-panda.webp"><img src="/media/img/red-panda.png" alt=""></picture>'
        markup = self._render("img/red-panda.png", [{"type": "image/webp", "srcset": {"img/red-panda.webp": "default"}}])
        self.assertEqual(markup, expected)

    def test_picture_type_media_srcset(self):
        """Should return expected markup when specifying type, media, and srcset"""
        expected = (
            "<picture>"
            '<source media="(max-width: 799px)" type="image/webp" srcset="/media/img/red-panda.webp">'
            '<source media="(max-width: 799px)" type="image/png" srcset="/media/img/red-panda.png">'
            '<img src="/media/img/red-panda.png" alt="">'
            "</picture>"
        )
        markup = self._render(
            "img/red-panda.png",
            [
                {"media": "(max-width: 799px)", "type": "image/webp", "srcset": {"img/red-panda.webp": "default"}},
                {"media": "(max-width: 799px)", "type": "image/png", "srcset": {"img/red-panda.png": "default"}},
            ],
        )
        self.assertEqual(markup, expected)

    def test_picture_type_srcset_sizes(self):
        """Should return expected markup when specifying type, srcset, and sizes"""
        expected = (
            "<picture>"
            '<source type="image/webp" srcset="/media/img/sleeping-panda-500.webp 500w,/media/img/sleeping-panda-1000.webp 1000w" '
            'sizes="(min-width: 1000px) calc(50vw - 200px),calc(100vw - 50px)">'
            '<source type="image/png" srcset="/media/img/sleeping-panda-500.png 500w,/media/img/sleeping-panda-1000.png 1000w" '
            'sizes="(min-width: 1000px) calc(50vw - 200px),calc(100vw - 50px)">'
            '<img src="/media/img/red-panda.png" alt="">'
            "</picture>"
        )
        markup = self._render(
            "img/red-panda.png",
            [
                {
                    "type": "image/webp",
                    "srcset": {"img/sleeping-panda-500.webp": "500w", "img/sleeping-panda-1000.webp": "1000w"},
                    "sizes": {"(min-width: 1000px)": "calc(50vw - 200px)", "default": "calc(100vw - 50px)"},
                },
                {
                    "type": "image/png",
                    "srcset": {"img/sleeping-panda-500.png": "500w", "img/sleeping-panda-1000.png": "1000w"},
                    "sizes": {"(min-width: 1000px)": "calc(50vw - 200px)", "default": "calc(100vw - 50px)"},
                },
            ],
        )
        self.assertEqual(markup, expected)

    def test_picture_l10n_images(self):
        """Should return expected markup when specifying L10n images"""
        expected = (
            "<picture>"
            '<source media="(max-width: 799px)" srcset="/media/img/l10n/en-US/panda-mobile.png">'
            '<source media="(min-width: 800px)" srcset="/media/img/l10n/en-US/panda-desktop.png">'
            '<img src="/media/img/l10n/en-US/panda-mobile.png" alt="">'
            "</picture>"
        )
        markup = self._render(
            "img/panda-mobile.png",
            [
                {"media": "(max-width: 799px)", "srcset": {"img/panda-mobile.png": "default"}},
                {"media": "(min-width: 800px)", "srcset": {"img/panda-desktop.png": "default"}},
            ],
            {"l10n": True},
        )
        self.assertEqual(markup, expected)

    def test_picture_with_optional_attributes(self):
        """Should return expected markup with optional attributes"""
        expected = (
            "<picture>"
            '<source media="(max-width: 799px)" srcset="/media/img/panda-mobile.png">'
            '<source media="(min-width: 800px)" srcset="/media/img/panda-desktop.png">'
            '<img src="/media/img/panda-mobile.png" alt="Red Panda" loading="lazy" class="panda-hero">'
            "</picture>"
        )
        markup = self._render(
            "img/panda-mobile.png",
            [
                {"media": "(max-width: 799px)", "srcset": {"img/panda-mobile.png": "default"}},
                {"media": "(min-width: 800px)", "srcset": {"img/panda-desktop.png": "default"}},
            ],
            {"alt": "Red Panda", "loading": "lazy", "class": "panda-hero"},
        )
        self.assertEqual(markup, expected)


class TestAbsoluteURLFilter(TestCase):
    rf = RequestFactory()
    static_url_dev = "/static/"
    static_url_prod = "//mozorg.cdn.mozilla.net/static/"
    static_url_full = "https://mozorg.cdn.mozilla.net/static/"
    image_path = "img/mozorg/mozilla-256.jpg"
    inline_template = "{{ static('%s')|absolute_url }}" % image_path
    block_template = "{% filter absolute_url %}{% block page_image %}" + "{{ static('%s') }}" % image_path + "{% endblock %}{% endfilter %}"

    def _render(self, template):
        return render(template, {"request": self.rf.get("/")})

    @patch("django.contrib.staticfiles.storage.staticfiles_storage.base_url", static_url_dev)
    def test_image_dev(self):
        """Should return a fully qualified URL including a protocol"""
        expected = settings.CANONICAL_URL + self.static_url_dev + self.image_path
        assert self._render(self.inline_template) == expected
        assert self._render(self.block_template) == expected

    @patch("django.contrib.staticfiles.storage.staticfiles_storage.base_url", static_url_prod)
    def test_image_prod(self):
        """Should return a fully qualified URL including a protocol"""
        expected = "https:" + self.static_url_prod + self.image_path
        assert self._render(self.inline_template) == expected
        assert self._render(self.block_template) == expected

    @override_settings(DEV=False)
    def test_urls(self):
        """Should return a fully qualified URL including a protocol"""
        expected = "https://www.mozilla.org/en-US/firefox/new/"
        assert misc.absolute_url("/en-US/firefox/new/") == expected
        assert misc.absolute_url("//www.mozilla.org/en-US/firefox/new/") == expected
        assert misc.absolute_url("https://www.mozilla.org/en-US/firefox/new/") == expected


class TestFirefoxIOSURL(TestCase):
    rf = RequestFactory()

    def _render(self, locale, ct_param=None):
        req = self.rf.get("/")
        req.locale = locale

        if ct_param:
            return render("{{ firefox_ios_url('%s') }}" % ct_param, {"request": req})

        return render("{{ firefox_ios_url() }}", {"request": req})

    def test_firefox_ios_url_no_locale(self):
        """No locale, fallback to default URL"""
        assert self._render("") == "https://itunes.apple.com/app/firefox-private-safe-browser/id989804926"

    def test_firefox_ios_url_default(self):
        """should fallback to default URL"""
        assert self._render("ar") == "https://itunes.apple.com/app/firefox-private-safe-browser/id989804926"
        assert self._render("zu") == "https://itunes.apple.com/app/firefox-private-safe-browser/id989804926"

    def test_firefox_ios_url_localized(self):
        """should return localized URL"""
        assert self._render("en-US") == "https://itunes.apple.com/us/app/firefox-private-safe-browser/id989804926"
        assert self._render("es-ES") == "https://itunes.apple.com/es/app/firefox-private-safe-browser/id989804926"
        assert self._render("ja") == "https://itunes.apple.com/jp/app/firefox-private-safe-browser/id989804926"

    def test_firefox_ios_url_param(self):
        """should return default or localized URL with ct param"""
        assert self._render("", "mozorg") == ("https://itunes.apple.com/app/firefox-private-safe-browser/id989804926?ct=mozorg")
        assert self._render("en-US", "mozorg") == ("https://itunes.apple.com/us/app/firefox-private-safe-browser/id989804926?ct=mozorg")
        assert self._render("es-ES", "mozorg") == ("https://itunes.apple.com/es/app/firefox-private-safe-browser/id989804926?ct=mozorg")


@pytest.mark.parametrize(
    "html, cleaned",
    [
        ("pre <script>alert('oops')</script> post", "pre alert('oops') post"),
        ("pre <script>alert('oops') post", "pre alert('oops') post"),
        ("pre <style>body {background-color: red;}</style> post", "pre body {background-color: red;} post"),
        ("pre <div onclick='foo()'></div> post", "pre  post"),
        ("pre <p>foo &amp; bar</p> post", "pre foo & bar post"),
        ("pre <p>mid</p> post", "pre mid post"),
    ],
)
def test_bleach_tags(html, cleaned):
    s = misc.bleach_tags(html)
    assert s == cleaned, f"{s} != {cleaned}"


def test_attrs():
    context = {"elem": BeautifulSoup("<h1>Test</h1>", "lxml")}
    template = "{% do elem.select('h1')|htmlattr(class='dude', id='abides',) %}{{ elem | safe }}"
    assert render(template, context) == '<html><body><h1 class="dude" id="abides">Test</h1></body></html>'


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Hello, World!", "hello-world"),
        (" multiple---dash and  space ", "multiple-dash-and-space"),
        ("underscore_in-value", "underscore_in-value"),
        ("spam & eggs", "spam-eggs"),
        ("__strip__underscore-value___", "strip__underscore-value"),
    ],
)
def test_slugify(text, expected):
    template = "{{ '%s' | slugify }}" % text
    assert render(template) == expected


# from jingo


def test_f():
    s = render('{{ "{0} : {z}"|f("a", z="b") }}')
    assert s == "a : b"


def test_f_unicode():
    s = render('{{ "foo {0}"|f(bar) }}', {"bar": "bar\xe9"})
    assert s == "foo bar\xe9"
    s = render("{{ t|f(bar) }}", {"t": "\xe9 {0}", "bar": "baz"})
    assert s == "\xe9 baz"


format_string = "Hello <b>{0}</b>"
format_markup = Markup(format_string)
val_string = "<em>Steve</em>"
val_markup = Markup(val_string)


@pytest.mark.parametrize(
    "f, v",
    [
        (format_string, val_string),
        (format_string, val_markup),
        (format_markup, val_string),
        (format_markup, val_markup),
    ],
)
def test_f_markup(f, v):
    expect = "Hello &lt;b&gt;&lt;em&gt;Steve&lt;/em&gt;&lt;/b&gt;"
    s = render("{{ fmt|f(val) }}", {"fmt": f, "val": v})
    assert expect == s


def test_datetime():
    time = datetime(2009, 12, 25, 10, 11, 12)
    s = render("{{ d|datetime }}", {"d": time})
    assert s == "December 25, 2009"

    s = render('{{ d|datetime("%Y-%m-%d %H:%M:%S") }}', {"d": time})
    assert s == "2009-12-25 10:11:12"

    s = render("{{ None|datetime }}")
    assert s == ""


def test_datetime_unicode():
    fmt = "%Y 年 %m 月 %e 日"
    misc.datetime(datetime.now(), fmt)


def test_ifeq():
    eq_context = {"a": 1, "b": 1}
    neq_context = {"a": 1, "b": 2}

    s = render('{{ a|ifeq(b, "<b>something</b>") }}', eq_context)
    assert s == "<b>something</b>"

    s = render('{{ a|ifeq(b, "<b>something</b>") }}', neq_context)
    assert s == ""


def test_csrf():
    s = render("{{ csrf() }}", {"csrf_token": "fffuuu"})
    csrf = '<input type="hidden" name="csrfmiddlewaretoken" value="fffuuu">'
    assert csrf in s


class TestAppStoreURL(TestCase):
    rf = RequestFactory()

    def _render(self, locale):
        req = self.rf.get("/")
        req.locale = locale
        product = "lockwise"
        return render("{{ app_store_url('%s') }}" % product, {"request": req})

    def test_app_store_url_no_locale(self):
        """No locale, fallback to default URL"""
        assert self._render("") == "https://itunes.apple.com/app/id1314000270?mt=8"

    def test_app_store_url_default(self):
        """should fallback to default URL"""
        assert self._render("ar") == "https://itunes.apple.com/app/id1314000270?mt=8"
        assert self._render("zu") == "https://itunes.apple.com/app/id1314000270?mt=8"

    def test_app_store_url_localized(self):
        """should return localized URL"""
        assert self._render("en-US") == "https://itunes.apple.com/us/app/id1314000270?mt=8"
        assert self._render("es-ES") == "https://itunes.apple.com/es/app/id1314000270?mt=8"
        assert self._render("de") == "https://itunes.apple.com/de/app/id1314000270?mt=8"


class TestPlayStoreURL(TestCase):
    rf = RequestFactory()

    def _render(self, locale):
        req = self.rf.get("/")
        req.locale = locale
        product = "lockwise"
        return render("{{ play_store_url('%s') }}" % product, {"request": req})

    def test_play_store_url_localized(self):
        """should return localized URL"""
        assert self._render("en-US") == "https://play.google.com/store/apps/details?id=mozilla.lockbox&amp;hl=en"
        assert self._render("es-ES") == "https://play.google.com/store/apps/details?id=mozilla.lockbox&amp;hl=es"
        assert self._render("de") == "https://play.google.com/store/apps/details?id=mozilla.lockbox&amp;hl=de"


class TestStructuredDataID(TestCase):
    rf = RequestFactory()

    def _render(self, locale, domain=None):
        req = self.rf.get("/")
        req.locale = locale
        sd_id = "firefoxbrowser"

        if domain:
            return render(f"{{{{ structured_data_id('{sd_id}', '{domain}') }}}}", {"request": req})

        return render("{{ structured_data_id('%s') }}" % sd_id, {"request": req})

    def test_structured_data_localized_id(self):
        """should return localized id"""
        assert self._render("en-US") == "https://www.mozilla.org/#firefoxbrowser"
        assert self._render("es-ES") == "https://www.mozilla.org/#firefoxbrowser-es-es"
        assert self._render("de") == "https://www.mozilla.org/#firefoxbrowser-de"

    def test_structured_data_custom_domain_id(self):
        """should return id for a custom domain"""
        domain = "https://foundation.mozilla.org"
        assert self._render("en-US", domain) == "https://foundation.mozilla.org/#firefoxbrowser"
        assert self._render("es-ES", domain) == "https://foundation.mozilla.org/#firefoxbrowser-es-es"
        assert self._render("de", domain) == "https://foundation.mozilla.org/#firefoxbrowser-de"


class TestLangShort(TestCase):
    rf = RequestFactory()

    def _render(self, locale, domain=None):
        req = self.rf.get("/")
        req.locale = locale

        return render("{{ lang_short() }}", {"request": req})

    def test_shortened_locales(self):
        """should return a shortened locale code"""
        assert self._render("en-US") == "en"
        assert self._render("es-ES") == "es"
        assert self._render("de") == "de"


class TestFirefoxAdjustUrl(TestCase):
    rf = RequestFactory()

    def _render(self, locale, redirect, adgroup, creative=None):
        req = self.rf.get("/")
        req.locale = locale

        if creative:
            return render(f"{{{{ firefox_adjust_url('{redirect}', '{adgroup}', '{creative}') }}}}", {"request": req})

        return render(f"{{{{ firefox_adjust_url('{redirect}', '{adgroup}') }}}}", {"request": req})

    def test_firefox_ios_adjust_url(self):
        """Firefox for mobile with an App Store URL redirect"""
        assert (
            self._render("en-US", "ios", "test-page") == "https://app.adjust.com/2uo1qc?redirect="
            "https%3A%2F%2Fitunes.apple.com%2Fus%2Fapp%2Ffirefox-private-safe-browser%2Fid989804926"
            "&amp;campaign=www.mozilla.org&amp;adgroup=test-page"
        )

    def test_firefox_ios_adjust_url_invalid_country(self):
        """Firefox for mobile with an App Store URL redirect with an unsupported country"""
        assert (
            self._render("zz", "ios", "test-page") == "https://app.adjust.com/2uo1qc?redirect="
            "https%3A%2F%2Fitunes.apple.com%2Fapp%2Ffirefox-private-safe-browser%2Fid989804926"
            "&amp;campaign=www.mozilla.org&amp;adgroup=test-page"
        )

    def test_firefox_ios_adjust_url_creative(self):
        """Firefox for mobile with an App Store URL redirect and creative param"""
        assert (
            self._render("de", "ios", "test-page", "experiment-name") == "https://app.adjust.com/2uo1qc?redirect="
            "https%3A%2F%2Fitunes.apple.com%2Fde%2Fapp%2Ffirefox-private-safe-browser%2Fid989804926"
            "&amp;campaign=www.mozilla.org&amp;adgroup=test-page&amp;creative=experiment-name"
        )

    def test_firefox_android_adjust_url(self):
        """Firefox for mobile with a Play Store redirect"""
        assert (
            self._render("en-US", "android", "test-page") == "https://app.adjust.com/2uo1qc?redirect="
            "https%3A%2F%2Fplay.google.com%2Fstore%2Fapps%2Fdetails%3Fid%3Dorg.mozilla.firefox"
            "&amp;campaign=www.mozilla.org&amp;adgroup=test-page"
        )

    def test_firefox_no_redirect_adjust_url(self):
        """Firefox for mobile with no redirect"""
        assert self._render("en-US", None, "test-page") == "https://app.adjust.com/2uo1qc?campaign=www.mozilla.org&amp;adgroup=test-page"


class TestFocusAdjustUrl(TestCase):
    rf = RequestFactory()

    def _render(self, locale, redirect, adgroup, creative=None):
        req = self.rf.get("/")
        req.locale = locale

        if creative:
            return render(f"{{{{ focus_adjust_url('{redirect}', '{adgroup}', '{creative}') }}}}", {"request": req})

        return render(f"{{{{ focus_adjust_url('{redirect}', '{adgroup}') }}}}", {"request": req})

    def test_focus_ios_adjust_url(self):
        """Firefox Focus with an App Store URL redirect"""
        assert (
            self._render("en-US", "ios", "test-page") == "https://app.adjust.com/b8s7qo?redirect="
            "https%3A%2F%2Fitunes.apple.com%2Fus%2Fapp%2Ffirefox-focus-privacy-browser%2Fid1055677337"
            "&amp;campaign=www.mozilla.org&amp;adgroup=test-page"
        )

    def test_focus_ios_adjust_url_invalid_country(self):
        """Firefox Focus with an App Store URL redirect with an unsupported country"""
        assert (
            self._render("zz", "ios", "test-page") == "https://app.adjust.com/b8s7qo?redirect="
            "https%3A%2F%2Fitunes.apple.com%2Fapp%2Ffirefox-focus-privacy-browser%2Fid1055677337"
            "&amp;campaign=www.mozilla.org&amp;adgroup=test-page"
        )

    def test_focus_ios_adjust_url_creative(self):
        """Firefox Focus with an App Store URL redirect and creative param"""
        assert (
            self._render("fr", "ios", "test-page", "experiment-name") == "https://app.adjust.com/b8s7qo?"
            "redirect=https%3A%2F%2Fitunes.apple.com%2Ffr%2Fapp%2Ffirefox-focus-privacy-browser%2Fid1055677337"
            "&amp;campaign=www.mozilla.org&amp;adgroup=test-page&amp;creative=experiment-name"
        )

    def test_focus_android_adjust_url(self):
        """Firefox Focus for mobile with a Play Store redirect"""
        assert (
            self._render("en-US", "android", "test-page") == "https://app.adjust.com/b8s7qo?redirect="
            "https%3A%2F%2Fplay.google.com%2Fstore%2Fapps%2Fdetails%3Fid%3Dorg.mozilla.focus"
            "&amp;campaign=www.mozilla.org&amp;adgroup=test-page"
        )

    def test_focus_no_redirect_adjust_url(self):
        """Firefox Focus for mobile with no redirect"""
        assert self._render("en-US", None, "test-page") == "https://app.adjust.com/b8s7qo?campaign=www.mozilla.org&amp;adgroup=test-page"

    def test_klar_ios_adjust_url(self):
        """Firefox Klar with an App Store URL redirect"""
        assert (
            self._render("de", "ios", "test-page") == "https://app.adjust.com/jfcx5x?redirect="
            "https%3A%2F%2Fitunes.apple.com%2Fde%2Fapp%2Fklar-by-firefox%2Fid1073435754"
            "&amp;campaign=www.mozilla.org&amp;adgroup=test-page"
        )

    def test_klar_android_adjust_url(self):
        """Firefox Klar for mobile with a Play Store redirect"""
        assert (
            self._render("de", "android", "test-page") == "https://app.adjust.com/jfcx5x?redirect="
            "https%3A%2F%2Fplay.google.com%2Fstore%2Fapps%2Fdetails%3Fid%3Dorg.mozilla.klar"
            "&amp;campaign=www.mozilla.org&amp;adgroup=test-page"
        )


class TestLockwiseAdjustUrl(TestCase):
    rf = RequestFactory()

    def _render(self, locale, redirect, adgroup, creative=None):
        req = self.rf.get("/")
        req.locale = locale

        if creative:
            return render(f"{{{{ lockwise_adjust_url('{redirect}', '{adgroup}', '{creative}') }}}}", {"request": req})

        return render(f"{{{{ lockwise_adjust_url('{redirect}', '{adgroup}') }}}}", {"request": req})

    def test_lockwise_ios_adjust_url(self):
        """Firefox Lockwise for mobile with an App Store URL redirect"""
        assert (
            self._render("en-US", "ios", "test-page") == "https://app.adjust.com/6tteyjo?redirect="
            "https%3A%2F%2Fitunes.apple.com%2Fus%2Fapp%2Fid1314000270%3Fmt%3D8"
            "&amp;campaign=www.mozilla.org&amp;adgroup=test-page"
        )

    def test_lockwise_ios_adjust_url_invalid_country(self):
        """Firefox Lockwise for mobile with an App Store URL redirect with an unsupported country"""
        assert (
            self._render("zz", "ios", "test-page") == "https://app.adjust.com/6tteyjo?redirect="
            "https%3A%2F%2Fitunes.apple.com%2Fapp%2Fid1314000270%3Fmt%3D8"
            "&amp;campaign=www.mozilla.org&amp;adgroup=test-page"
        )

    def test_lockwise_ios_adjust_url_creative(self):
        """Firefox Lockwise for mobile with an App Store URL redirect and creative param"""
        assert (
            self._render("de", "ios", "test-page", "experiment-name") == "https://app.adjust.com/6tteyjo"
            "?redirect=https%3A%2F%2Fitunes.apple.com%2Fde%2Fapp%2Fid1314000270%3Fmt%3D8"
            "&amp;campaign=www.mozilla.org&amp;adgroup=test-page&amp;creative=experiment-name"
        )

    def test_lockwise_android_adjust_url(self):
        """Firefox Lockwise for mobile with a Play Store redirect"""
        assert (
            self._render("en-US", "android", "test-page") == "https://app.adjust.com/6tteyjo?redirect="
            "https%3A%2F%2Fplay.google.com%2Fstore%2Fapps%2Fdetails%3Fid%3Dmozilla.lockbox"
            "&amp;campaign=www.mozilla.org&amp;adgroup=test-page"
        )

    def test_lockwise_no_redirect_adjust_url(self):
        """Firefox Lockwise for mobile with no redirect"""
        assert self._render("en-US", None, "test-page") == "https://app.adjust.com/6tteyjo?campaign=www.mozilla.org&amp;adgroup=test-page"


class TestPocketAdjustUrl(TestCase):
    rf = RequestFactory()

    def _render(self, locale, redirect, adgroup, creative=None):
        req = self.rf.get("/")
        req.locale = locale

        if creative:
            return render(f"{{{{ pocket_adjust_url('{redirect}', '{adgroup}', '{creative}') }}}}", {"request": req})

        return render(f"{{{{ pocket_adjust_url('{redirect}', '{adgroup}') }}}}", {"request": req})

    def test_pocket_ios_adjust_url(self):
        """Pocket for mobile with an App Store URL redirect"""
        assert (
            self._render("en-US", "ios", "test-page") == "https://app.adjust.com/m54twk?redirect="
            "https%3A%2F%2Fitunes.apple.com%2Fus%2Fapp%2Fpocket-save-read-grow%2Fid309601447"
            "&amp;campaign=www.mozilla.org&amp;adgroup=test-page"
        )

    def test_pocket_ios_adjust_url_invalid_country(self):
        """Pocket for mobile with an App Store URL redirect with an unsupported country"""
        assert (
            self._render("zz", "ios", "test-page") == "https://app.adjust.com/m54twk?redirect="
            "https%3A%2F%2Fitunes.apple.com%2Fapp%2Fpocket-save-read-grow%2Fid309601447"
            "&amp;campaign=www.mozilla.org&amp;adgroup=test-page"
        )

    def test_pocket_ios_adjust_url_creative(self):
        """Pocket for mobile with an App Store URL redirect and creative param"""
        assert (
            self._render("de", "ios", "test-page", "experiment-name") == "https://app.adjust.com/m54twk?redirect="
            "https%3A%2F%2Fitunes.apple.com%2Fde%2Fapp%2Fpocket-save-read-grow%2Fid309601447"
            "&amp;campaign=www.mozilla.org&amp;adgroup=test-page&amp;creative=experiment-name"
        )

    def test_pocket_android_adjust_url(self):
        """Pocket for mobile with a Play Store redirect"""
        assert (
            self._render("en-US", "android", "test-page") == "https://app.adjust.com/m54twk?redirect="
            "https%3A%2F%2Fplay.google.com%2Fstore%2Fapps%2Fdetails%3Fid%3Dcom.ideashower.readitlater.pro"
            "&amp;campaign=www.mozilla.org&amp;adgroup=test-page"
        )

    def test_pocket_no_redirect_adjust_url(self):
        """Pocket for mobile with no redirect"""
        assert self._render("en-US", None, "test-page") == "https://app.adjust.com/m54twk?campaign=www.mozilla.org&amp;adgroup=test-page"


@override_settings(FXA_ENDPOINT=TEST_FXA_ENDPOINT)
class TestRelayFxAButton(TestCase):
    rf = RequestFactory()

    def _render(
        self,
        entrypoint,
        button_text,
        class_name=None,
        is_button_class=True,
        include_metrics=True,
        optional_parameters=None,
        optional_attributes=None,
    ):
        req = self.rf.get("/")
        req.locale = "en-US"
        return render(
            "{{{{ relay_fxa_button('{0}', '{1}', '{2}', {3}, {4}, {5}, {6}) }}}}".format(
                entrypoint, button_text, class_name, is_button_class, include_metrics, optional_parameters, optional_attributes
            ),
            {"request": req},
        )

    def test_relay_fxa_button(self):
        """Should return expected markup"""
        markup = self._render(
            entrypoint="mozilla.org-whatsnew",
            button_text="Sign In to Relay",
            class_name="relay-main-cta-button",
            is_button_class=True,
            include_metrics=True,
            optional_parameters={"utm_campaign": "whatsnew96"},
            optional_attributes={"data-cta-text": "Sign In to Relay", "data-cta-type": "fxa-relay", "data-cta-position": "primary"},
        )
        expected = (
            '<a href="https://relay.firefox.com/accounts/fxa/login/?process=login&entrypoint=mozilla.org-whatsnew&form_type=button'
            '&utm_source=mozilla.org-whatsnew&utm_medium=referral&utm_campaign=whatsnew96" data-action="https://accounts.firefox.com/" '
            'class="js-fxa-cta-link js-fxa-product-button mzp-c-button mzp-t-product relay-main-cta-button" '
            'data-cta-text="Sign In to Relay" data-cta-type="fxa-relay" data-cta-position="primary">Sign In to Relay</a>'
        )
        self.assertEqual(markup, expected)


@override_settings(FXA_ENDPOINT=TEST_FXA_ENDPOINT)
class TestPocketFxAButton(TestCase):
    rf = RequestFactory()

    def _render(
        self, entrypoint, button_text, class_name=None, is_button_class=True, include_metrics=True, optional_parameters=None, optional_attributes=None
    ):
        req = self.rf.get("/")
        req.locale = "en-US"
        return render(
            "{{{{ pocket_fxa_button('{0}', '{1}', '{2}', {3}, {4}, {5}, {6}) }}}}".format(
                entrypoint, button_text, class_name, is_button_class, include_metrics, optional_parameters, optional_attributes
            ),
            {"request": req},
        )

    def test_pocket_fxa_button(self):
        """Should return expected markup"""
        markup = self._render(
            entrypoint="mozilla.org-firefox-pocket",
            button_text="Try Pocket Now",
            class_name="pocket-main-cta-button",
            is_button_class=True,
            include_metrics=True,
            optional_parameters={"s": "ffpocket", "foo": "bar"},
            optional_attributes={"data-cta-text": "Try Pocket Now", "data-cta-type": "activate pocket", "data-cta-position": "primary"},
        )
        expected = (
            '<a href="https://getpocket.com/ff_signup?entrypoint=mozilla.org-firefox-pocket&form_type=button'
            '&utm_source=mozilla.org-firefox-pocket&utm_medium=referral&s=ffpocket&foo=bar" data-action="https://accounts.firefox.com/" '
            'class="js-fxa-cta-link js-fxa-product-button mzp-c-button mzp-t-product pocket-main-cta-button" '
            'data-cta-text="Try Pocket Now" data-cta-type="activate pocket" data-cta-position="primary">Try Pocket Now</a>'
        )
        self.assertEqual(markup, expected)


@override_settings(FXA_ENDPOINT=TEST_FXA_ENDPOINT)
class TestMonitorFxAButton(TestCase):
    rf = RequestFactory()

    def _render(
        self,
        entrypoint,
        button_text,
        class_name=None,
        is_button_class=False,
        include_metrics=True,
        optional_parameters=None,
        optional_attributes=None,
    ):
        req = self.rf.get("/")
        req.locale = "en-US"
        return render(
            "{{{{ monitor_fxa_button('{0}', '{1}', '{2}', {3}, {4}, {5}, {6}) }}}}".format(
                entrypoint, button_text, class_name, is_button_class, include_metrics, optional_parameters, optional_attributes
            ),
            {"request": req},
        )

    def test_monitor_fxa_button(self):
        """Should return expected markup"""
        markup = self._render(
            entrypoint="mozilla.org-firefox-accounts",
            button_text="Sign In to Monitor",
            class_name="monitor-main-cta-button",
            is_button_class=False,
            include_metrics=True,
            optional_parameters={"utm_campaign": "skyline"},
            optional_attributes={"data-cta-text": "Sign In to Monitor", "data-cta-type": "fxa-monitor", "data-cta-position": "primary"},
        )
        expected = (
            '<a href="https://monitor.firefox.com/oauth/init?entrypoint=mozilla.org-firefox-accounts&form_type=button'
            '&utm_source=mozilla.org-firefox-accounts&utm_medium=referral&utm_campaign=skyline" '
            'data-action="https://accounts.firefox.com/" class="js-fxa-cta-link js-fxa-product-button '
            'monitor-main-cta-button" data-cta-text="Sign In to Monitor" data-cta-type="fxa-monitor" '
            'data-cta-position="primary">Sign In to Monitor</a>'
        )
        self.assertEqual(markup, expected)


@override_settings(FXA_ENDPOINT=TEST_FXA_ENDPOINT)
class TestFxAButton(TestCase):
    rf = RequestFactory()

    def _render(
        self,
        entrypoint,
        button_text,
        action="signup",
        class_name=None,
        is_button_class=True,
        include_metrics=True,
        optional_parameters=None,
        optional_attributes=None,
    ):
        req = self.rf.get("/")
        req.locale = "en-US"
        return render(
            "{{{{ fxa_button('{0}', '{1}', '{2}', '{3}', {4}, {5}, {6}, {7}) }}}}".format(
                entrypoint, button_text, action, class_name, is_button_class, include_metrics, optional_parameters, optional_attributes
            ),
            {"request": req},
        )

    def test_fxa_button_signup(self):
        """Should return expected markup"""
        markup = self._render(
            entrypoint="mozilla.org-firefox-whatsnew73",
            button_text="Sign Up",
            action="signup",
            class_name="fxa-main-cta-button",
            is_button_class=True,
            include_metrics=True,
            optional_parameters={"utm_campaign": "whatsnew73"},
            optional_attributes={"data-cta-text": "Sign Up", "data-cta-type": "fxa-sync", "data-cta-position": "primary"},
        )
        expected = (
            '<a href="https://accounts.firefox.com/signup?entrypoint=mozilla.org-firefox-whatsnew73&form_type=button'
            '&utm_source=mozilla.org-firefox-whatsnew73&utm_medium=referral&utm_campaign=whatsnew73" '
            'data-action="https://accounts.firefox.com/" class="js-fxa-cta-link js-fxa-product-button mzp-c-button mzp-t-product '
            'fxa-main-cta-button" data-cta-text="Sign Up" data-cta-type="fxa-sync" data-cta-position="primary">Sign Up</a>'
        )
        self.assertEqual(markup, expected)

    def test_fxa_button_signin(self):
        """Should return expected markup"""
        markup = self._render(
            entrypoint="mozilla.org-firefox-whatsnew73",
            button_text="Sign In",
            action="signin",
            class_name="fxa-main-cta-button",
            is_button_class=True,
            include_metrics=True,
            optional_parameters={"utm_campaign": "whatsnew73"},
            optional_attributes={"data-cta-text": "Sign In", "data-cta-type": "fxa-sync", "data-cta-position": "primary"},
        )
        expected = (
            '<a href="https://accounts.firefox.com/signin?entrypoint=mozilla.org-firefox-whatsnew73&form_type=button'
            '&utm_source=mozilla.org-firefox-whatsnew73&utm_medium=referral&utm_campaign=whatsnew73" '
            'data-action="https://accounts.firefox.com/" class="js-fxa-cta-link js-fxa-product-button mzp-c-button mzp-t-product '
            'fxa-main-cta-button" data-cta-text="Sign In" data-cta-type="fxa-sync" data-cta-position="primary">Sign In</a>'
        )
        self.assertEqual(markup, expected)

    def test_fxa_button_email(self):
        """Should return expected markup"""
        markup = self._render(
            entrypoint="mozilla.org-firefox-whatsnew73",
            button_text="Sign Up",
            action="email",
            class_name="fxa-main-cta-button",
            is_button_class=True,
            include_metrics=True,
            optional_parameters={"utm_campaign": "whatsnew73"},
            optional_attributes={"data-cta-text": "Sign Up", "data-cta-type": "fxa-sync", "data-cta-position": "primary"},
        )
        expected = (
            '<a href="https://accounts.firefox.com/?action=email&entrypoint=mozilla.org-firefox-whatsnew73&form_type=button'
            '&utm_source=mozilla.org-firefox-whatsnew73&utm_medium=referral&utm_campaign=whatsnew73" '
            'data-action="https://accounts.firefox.com/" class="js-fxa-cta-link js-fxa-product-button mzp-c-button mzp-t-product '
            'fxa-main-cta-button" data-cta-text="Sign Up" data-cta-type="fxa-sync" data-cta-position="primary">Sign Up</a>'
        )
        self.assertEqual(markup, expected)


@override_settings(FXA_ENDPOINT=TEST_FXA_ENDPOINT)
class TestFxALinkFragment(TestCase):
    rf = RequestFactory()

    def _render(self, entrypoint, action="signup", optional_parameters=None):
        req = self.rf.get("/")
        req.locale = "en-US"
        return render(f"{{{{ fxa_link_fragment('{entrypoint}', '{action}', {optional_parameters}) }}}}", {"request": req})

    def test_fxa_button_signup(self):
        """Should return expected markup"""
        markup = self._render(entrypoint="mozilla.org-firefox-whatsnew73", action="signup", optional_parameters={"utm_campaign": "whatsnew73"})
        expected = (
            'href="https://accounts.firefox.com/signup?entrypoint=mozilla.org-firefox-whatsnew73&form_type=button'
            '&utm_source=mozilla.org-firefox-whatsnew73&utm_medium=referral&utm_campaign=whatsnew73"'
        )
        self.assertEqual(markup, expected)

    def test_fxa_button_email(self):
        """Should return expected markup"""
        markup = self._render(entrypoint="mozilla.org-firefox-whatsnew73", action="email", optional_parameters={"utm_campaign": "whatsnew73"})
        expected = (
            'href="https://accounts.firefox.com/?action=email&entrypoint=mozilla.org-firefox-whatsnew73&form_type=button'
            '&utm_source=mozilla.org-firefox-whatsnew73&utm_medium=referral&utm_campaign=whatsnew73"'
        )
        self.assertEqual(markup, expected)
