# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from unittest.mock import patch

from django.test import TestCase, override_settings
from django.utils.safestring import SafeData, mark_safe

import pytest
from django_jinja.backend import Jinja2
from markupsafe import Markup

from bedrock.base.templatetags import helpers
from lib.l10n_utils import get_translations_native_names

jinja_env = Jinja2.get_default()
SEND_TO_DEVICE_MESSAGE_SETS = {
    "default": {
        "email": {
            "android": "download-firefox-android",
            "ios": "download-firefox-ios",
            "all": "download-firefox-mobile",
        }
    }
}


def render(s, context={}):
    t = jinja_env.from_string(s)
    return t.render(context)


class HelpersTests(TestCase):
    def test_urlencode_with_unicode(self):
        template = '<a href="?var={{ key|urlencode }}">'
        context = {"key": "?& /()"}
        assert render(template, context) == '<a href="?var=%3F%26+%2F%28%29">'
        # non-ascii
        context = {"key": "\xe4"}
        assert render(template, context) == '<a href="?var=%C3%A4">'

    def test_mailtoencode_with_unicode(self):
        template = '<a href="?var={{ key|mailtoencode }}">'
        context = {"key": "?& /()"}
        assert render(template, context) == '<a href="?var=%3F%26%20/%28%29">'
        # non-ascii
        context = {"key": "\xe4"}
        assert render(template, context) == '<a href="?var=%C3%A4">'

    def test_add_bedrock_attributes(self):
        fresh_html = """
            <html>
            <body>
                <h1>Test h1</h1>
                <p>No change</p>
                <h2>Test h2 one</h2>
                <ul>
                    <li>one</li>
                </ul>
                <h2>Test h2 two</h2>
                <ol>
                    <li>two</li>
                </ol>
                <h3>Test @#$% h3</h3>
                <p>Here is an <a href="https://example.com">external link</a></p>
            </body>
        </html>
        """
        expected_html = """
<html>
<body>
<h1 id="test-h1">Test h1</h1>
<p>No change</p>
<h2 id="test-h2-one">Test h2 one</h2>
<ul class="mzp-u-list-styled">
<li>one</li>
</ul>
<h2 id="test-h2-two">Test h2 two</h2>
<ol class="mzp-u-list-styled">
<li>two</li>
</ol>
<h3 id="test-h3">Test @#$% h3</h3>
<p>Here is an <a href="https://example.com" rel="external noopener" target="_blank">external link</a></p>
</body>
</html>
"""
        processed_html = helpers.add_bedrock_attributes(fresh_html)
        assert processed_html == expected_html


class TestAddCtaAnalytics:
    ANALYTICS_ID = "test-uuid-1234"

    def test_adds_attributes_to_links(self):
        html = '<div class="rich-text"><p>Click <a href="https://example.com">here</a></p></div>'
        result = helpers.add_cta_analytics(html, self.ANALYTICS_ID)
        assert 'data-cta-text="here"' in result
        assert f'data-cta-uid="{self.ANALYTICS_ID}"' in result

    def test_multiple_links_all_get_attributes(self):
        link1 = '<a href="https://a.com">First</a>'
        link2 = '<a href="https://b.com">Second</a>'
        html = f"<p>{link1} and {link2}</p>"

        link1_expected_result = link1.replace("<a ", f'<a data-cta-text="First" data-cta-uid="{self.ANALYTICS_ID}" ')
        link2_expected_result = link2.replace("<a ", f'<a data-cta-text="Second" data-cta-uid="{self.ANALYTICS_ID}" ')
        expected_result = f"<p>{link1_expected_result} and {link2_expected_result}</p>"

        result = helpers.add_cta_analytics(html, self.ANALYTICS_ID)

        assert result.count(f'data-cta-uid="{self.ANALYTICS_ID}"') == 2
        assert expected_result == result

    def test_nested_markup_in_link_text_is_stripped(self):
        html = '<p><a href="https://example.com"><strong>bold link</strong></a></p>'

        expected_result = html.replace("<a ", f'<a data-cta-text="bold link" data-cta-uid="{self.ANALYTICS_ID}" ')
        result = helpers.add_cta_analytics(html, self.ANALYTICS_ID)

        assert 'data-cta-text="bold link"' in result
        assert result == expected_result

    def test_no_links_returns_unchanged_content(self):
        html = '<div class="rich-text"><p>No links here</p></div>'
        result = helpers.add_cta_analytics(html, self.ANALYTICS_ID)
        assert self.ANALYTICS_ID not in result
        assert "data-cta" not in result

    def test_does_not_add_html_body_wrappers_div_fragment(self):
        html = '<div class="rich-text"><p><a href="https://example.com">link</a></p></div>'
        result = helpers.add_cta_analytics(html, self.ANALYTICS_ID)
        assert "<html>" not in result
        assert "<body>" not in result
        assert result.startswith("<div")

    def test_does_not_add_html_body_wrappers_bare_link(self):
        html = '<a href="https://example.com">link</a>'
        result = helpers.add_cta_analytics(html, self.ANALYTICS_ID)
        assert "<html>" not in result
        assert "<body>" not in result
        assert result.startswith("<a")

    def test_does_not_add_html_body_wrappers_no_links(self):
        html = '<div class="rich-text"><p>No links here</p></div>'
        result = helpers.add_cta_analytics(html, self.ANALYTICS_ID)
        assert "<html>" not in result
        assert "<body>" not in result
        assert result.startswith("<div")

    def test_safe_input_returns_safe_output(self):
        html = mark_safe('<p><a href="https://example.com">link</a></p>')
        result = helpers.add_cta_analytics(html, self.ANALYTICS_ID)
        assert isinstance(result, SafeData)

    def test_markup_input_returns_safe_output(self):
        html = Markup('<p><a href="https://example.com">link</a></p>')
        result = helpers.add_cta_analytics(html, self.ANALYTICS_ID)
        assert isinstance(result, SafeData)

    def test_plain_string_input_returns_plain_string(self):
        html = '<p><a href="https://example.com">link</a></p>'
        result = helpers.add_cta_analytics(html, self.ANALYTICS_ID)
        assert not isinstance(result, (SafeData, Markup))

    def test_empty_analytics_id_returns_html_unchanged(self):
        html = '<p><a href="https://example.com">link</a></p>'
        result = helpers.add_cta_analytics(html, "")
        assert "data-cta" not in result
        assert result == html

    def test_none_analytics_id_returns_html_unchanged(self):
        html = '<p><a href="https://example.com">link</a></p>'
        result = helpers.add_cta_analytics(html, None)
        assert "data-cta" not in result
        assert result == html


@override_settings(LANG_GROUPS={"en": ["en-US", "en-GB"]})
def test_switch():
    with patch.object(helpers, "waffle") as waffle:
        ret = helpers.switch({"LANG": "de"}, "dude", ["fr", "de"])

    assert ret is waffle.switch.return_value
    waffle.switch.assert_called_with("dude")

    with patch.object(helpers, "waffle") as waffle:
        assert not helpers.switch({"LANG": "de"}, "dude", ["fr", "en"])

    waffle.switch.assert_not_called()

    with patch.object(helpers, "waffle") as waffle:
        ret = helpers.switch({"LANG": "de"}, "dude")

    assert ret is waffle.switch.return_value
    waffle.switch.assert_called_with("dude")

    with patch.object(helpers, "waffle") as waffle:
        ret = helpers.switch({"LANG": "en-GB"}, "dude", ["de", "en"])

    assert ret is waffle.switch.return_value
    waffle.switch.assert_called_with("dude")


@override_settings(FALLBACK_LOCALES={})
@pytest.mark.parametrize(
    "translations_locales, cms_locales, django_locales, expected",
    (
        (
            ["en-US", "fr", "sco"],
            ["de", "pt-BR"],
            ["ja-JP", "zh-CN"],
            ["de", "pt-BR", "ja-JP", "zh-CN"],
        ),
        (
            # Just use defaults
            ["en-US", "fr", "sco"],
            [],
            [],
            ["en-US", "fr", "sco"],
        ),
        (
            # Don't use CMS + Django Fallback
            ["en-US", "fr", "sco"],
            ["en-US", "de"],
            [],
            ["en-US", "fr", "sco"],
        ),
        (
            # Don't use CMS + Django Fallback
            ["en-US", "fr", "sco"],
            [],
            ["en-US", "de"],
            ["en-US", "fr", "sco"],
        ),
    ),
)
def test_get_locale_options(rf, translations_locales, cms_locales, django_locales, expected):
    native_translations = get_translations_native_names(translations_locales)
    native_expected = get_translations_native_names(expected)
    request = rf.get("/dummy/path/")

    if cms_locales is not None:
        request._locales_available_via_cms = cms_locales

    if django_locales is not None:
        request._locales_for_django_fallback_view = django_locales

    assert native_expected == helpers.get_locale_options(
        request=request,
        translations=native_translations,
    )


@override_settings(FALLBACK_LOCALES={"es-AR": "es-ES", "es-CL": "es-ES"})
def test_get_locale_options_adds_alias_locales_when_fallback_present(rf):
    """Alias locales whose fallback is in translations are added to the language picker.

    For pure Fluent pages, translations only reflects FTL-active locales. When a
    fallback locale (e.g. es-ES) is present, its aliases (es-AR, es-CL) must also
    appear so the language picker offers them to users browsing those locales.
    """
    request = rf.get("/dummy/path/")
    translations = get_translations_native_names(["en-US", "es-ES", "fr"])

    result = helpers.get_locale_options(request=request, translations=translations)

    assert "es-AR" in result
    assert "es-CL" in result
    assert "en-US" in result
    assert "es-ES" in result
    assert "fr" in result


@override_settings(FALLBACK_LOCALES={"es-AR": "es-ES"})
def test_get_locale_options_does_not_add_alias_when_fallback_absent(rf):
    """Alias locales are not added when their fallback locale is not in translations."""
    request = rf.get("/dummy/path/")
    translations = get_translations_native_names(["en-US", "fr"])  # no es-ES

    result = helpers.get_locale_options(request=request, translations=translations)

    assert "es-AR" not in result


@override_settings(FALLBACK_LOCALES={"es-AR": "es-ES"})
def test_get_locale_options_does_not_double_add_alias_already_present(rf):
    """Alias locales are not duplicated when already present (e.g. from CMS path)."""
    # Simulate CMS page where get_locales_for_cms_page() already added es-AR.
    translations_locales = ["en-US", "es-ES", "es-AR"]
    native_translations = get_translations_native_names(translations_locales)
    request = rf.get("/dummy/path/")

    result = helpers.get_locale_options(request=request, translations=native_translations)

    assert len(result) == len(translations_locales)
    for key in translations_locales:
        assert list(result).count(key) == 1  # no duplicate
