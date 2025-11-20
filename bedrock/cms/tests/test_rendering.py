# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Test the way Wagtail pages are handled by lib.l10n_utils.render

# The pytest fixtures used to run these tests are defined in bedrock/cms/tests/conftest.py

from django.conf import settings

import pytest
from wagtail.models import Locale, Page, Site
from wagtail.models.i18n import get_content_languages

from bedrock.cms.tests.factories import LocaleFactory, SimpleRichTextPageFactory
from lib import l10n_utils

pytestmark = [
    pytest.mark.django_db,
]


def test_locale_redirect_logic_is_skipped_for_cms_page(
    minimal_site,
    mocker,
    rf,
):
    "Confirm that CMS pages with the lang code in the path get served fine"

    mocker.patch("lib.l10n_utils.redirect_to_locale")
    mocker.patch("lib.l10n_utils.redirect_to_best_locale")

    page = Page.objects.last().specific

    _relative_url = page.relative_url(minimal_site)
    assert _relative_url == "/en-US/test-page/"
    request = rf.get(_relative_url)

    resp = page.serve(request)
    assert "Test Page" in resp.text

    l10n_utils.redirect_to_locale.assert_not_called()
    l10n_utils.redirect_to_best_locale.assert_not_called()


def test_locale_redirect_will_work_for_cms_pages(
    minimal_site,
    mocker,
    rf,
):
    """Confirm that CMS pages with the lang code in the path get
    redirected before being served fine"""

    redirect_to_locale_spy = mocker.spy(l10n_utils, "redirect_to_locale")
    redirect_to_best_locale_spy = mocker.spy(l10n_utils, "redirect_to_best_locale")

    page = Page.objects.last().specific

    assert page.url_path == "/test-page/"  # i.e., no lang code
    request = rf.get(page.url_path)

    resp = page.serve(request)

    assert resp.headers["location"] == "/en-US/test-page/"
    assert redirect_to_locale_spy.call_count == 1
    assert redirect_to_best_locale_spy.call_count == 0


def test_locale_redirect_will_work_for_cms_pages__default_locale_not_available(
    minimal_site,
    mocker,
    rf,
):
    redirect_to_locale_spy = mocker.spy(l10n_utils, "redirect_to_locale")
    redirect_to_best_locale_spy = mocker.spy(l10n_utils, "redirect_to_best_locale")

    page = Page.objects.last().specific
    fr_locale = Locale.objects.get(language_code="fr")

    assert settings.LANGUAGE_CODE != fr_locale.language_code

    page.locale = fr_locale
    page.save()

    assert page.url_path == "/test-page/"  # i.e., no lang code
    request = rf.get(page.url_path)

    resp = page.serve(request)

    assert resp.headers["location"] == "/fr/test-page/"  # NB not en-US
    assert redirect_to_locale_spy.call_count == 1
    assert redirect_to_best_locale_spy.call_count == 1


@pytest.mark.parametrize("serving_method", ("serve", "serve_preview"))
def test_locales_are_drawn_from_page_translations(minimal_site, rf, serving_method):
    assert Locale.objects.count() == 2  # en-US and fr
    fr_locale = Locale.objects.get(language_code="fr")

    page = Page.objects.last().specific
    fr_page = page.copy_for_translation(fr_locale)
    fr_page.title = "FR test page"
    rev = fr_page.save_revision()
    fr_page.publish(rev)
    assert fr_page.locale.language_code == "fr"

    _relative_url = page.relative_url(minimal_site)
    assert _relative_url == "/en-US/test-page/"
    request = rf.get(_relative_url)

    resp = getattr(page, serving_method)(request)
    page_content = resp.text
    assert "Test Page" in page_content
    assert '<option lang="en-US" value="en-US" selected>English</option>' in page_content
    assert '<option lang="fr" value="fr">Français</option>'.encode() in resp.content
    assert '<option lang="en-GB" value="en-US">English (British) </option>' not in page_content


@pytest.mark.django_db
class TestWagtailMixedCaseLocaleOrderBug:
    """
    Tests that demonstrate the Wagtail locale order bug where the order of
    languages in WAGTAIL_CONTENT_LANGUAGES affects which page is served for
    mixed-case locale codes like es-ES.

    The bug occurs because:
    1. Django normalizes 'es-ES' to lowercase 'es-es' internally
    2. Wagtail's get_supported_content_language_variant() tries to match 'es-es'
    3. When exact match fails, it falls back to the FIRST 'es-*' locale in
       WAGTAIL_CONTENT_LANGUAGES
    4. If 'es-AR' comes before 'es-ES', it returns 'es-AR' instead of 'es-ES'
    """

    def test_es_ES_works_when_only_spanish_locale(self, client, settings):
        """
        Test that es-ES pages work correctly when es-ES is the only Spanish
        locale in WAGTAIL_CONTENT_LANGUAGES.
        """

        # Override settings to have only es-ES as Spanish locale
        settings.WAGTAIL_CONTENT_LANGUAGES = [
            ("en-US", "English (US)"),
            ("de", "German"),
            ("fr", "French"),
            ("es-ES", "Spanish (Spain)"),  # Only es-* locale
            ("ja", "Japanese"),
        ]

        # Clear the cache so it picks up our override
        get_content_languages.cache_clear()

        # Create locales
        en_us_locale = Locale.objects.get(language_code="en-US")
        es_es_locale = LocaleFactory(language_code="es-ES")

        # Set up site and pages - need to create translated root first
        site = Site.objects.get(is_default_site=True)
        en_us_root = site.root_page

        # Create translated root page for es-ES
        es_es_root = en_us_root.copy_for_translation(es_es_locale)
        rev = es_es_root.save_revision()
        es_es_root.publish(rev)

        # Create en-US page with distinctive content
        en_us_page = SimpleRichTextPageFactory(
            title="Test Page English",
            slug="test-page",
            parent=en_us_root,
            locale=en_us_locale,
            content="This is the English version UNIQUE_EN_MARKER",
        )

        # Create es-ES translation with distinctive content
        es_es_page = en_us_page.copy_for_translation(es_es_locale)
        es_es_page.title = "Página de prueba"
        es_es_page.content = "Esta es la versión en español UNIQUE_ES_ES_MARKER"
        es_es_page.save()
        rev = es_es_page.save_revision()
        es_es_page.publish(rev)

        # Verify the page was created correctly
        assert es_es_page.locale.language_code == "es-ES"

        # Refresh to get the live status
        es_es_page.refresh_from_db()
        assert es_es_page.live is True, f"es-ES page should be live, but live={es_es_page.live}"

        # Make request to es-ES page
        response = client.get(es_es_page.url)

        assert response.status_code == 200
        html_content = response.content.decode()

        # Should serve Spanish content
        assert "UNIQUE_ES_ES_MARKER" in html_content, "es-ES content not found - English page was served instead"
        assert "Página de prueba" in html_content, "es-ES title not found"

        # Should NOT serve English content
        assert "UNIQUE_EN_MARKER" not in html_content, "Found English content when requesting es-ES URL"

    def test_es_ES_fails_when_es_AR_comes_first(self, client, settings):
        """
        Test that demonstrates the bug: when es-AR comes before es-ES in
        WAGTAIL_CONTENT_LANGUAGES, the wrong page content is served.
        """

        # Override settings to have es-AR before es-ES
        settings.WAGTAIL_CONTENT_LANGUAGES = [
            ("en-US", "English (US)"),
            ("de", "German"),
            ("fr", "French"),
            ("es-AR", "Español (de Argentina)"),  # First es-* locale
            ("es-ES", "Español (de España)"),  # Second es-* locale
            ("ja", "Japanese"),
        ]

        # Clear the cache so it picks up our override
        get_content_languages.cache_clear()

        # Create locales - note we're NOT creating es-AR locale
        # We only create es-ES to show that even with the locale existing,
        # the page serves wrong content due to the ordering bug
        en_us_locale = Locale.objects.get(language_code="en-US")
        es_es_locale = LocaleFactory(language_code="es-ES")

        # Set up site and pages - need to create translated root first
        site = Site.objects.get(is_default_site=True)
        en_us_root = site.root_page

        # Create translated root page for es-ES
        es_es_root = en_us_root.copy_for_translation(es_es_locale)
        rev = es_es_root.save_revision()
        es_es_root.publish(rev)

        # Create en-US page with distinctive content
        en_us_page = SimpleRichTextPageFactory(
            title="Test Page English",
            slug="test-page",
            parent=en_us_root,
            locale=en_us_locale,
            content="This is the English version UNIQUE_EN_MARKER",
        )

        # Create es-ES translation with distinctive content
        es_es_page = en_us_page.copy_for_translation(es_es_locale)
        es_es_page.title = "Página de prueba España"
        es_es_page.content = "Esta es la versión en español de España UNIQUE_ES_ES_MARKER"
        es_es_page.save()
        rev = es_es_page.save_revision()
        es_es_page.publish(rev)

        # Verify the page was created correctly
        assert es_es_page.locale.language_code == "es-ES"

        # Refresh to get the live status
        es_es_page.refresh_from_db()
        assert es_es_page.live is True, f"es-ES page should be live, but live={es_es_page.live}"

        # Make request to es-ES page
        response = client.get(es_es_page.url)

        # The response should have the es-ES content (not es-AR content or en-US content).
        assert response.status_code == 200
        html_content = response.content.decode()

        assert "UNIQUE_ES_ES_MARKER" in html_content
        assert "Página de prueba España" in html_content, "es-ES title not found"

        # Should NOT serve English content
        assert "UNIQUE_EN_MARKER" not in html_content, (
            "Found English content when requesting es-ES URL - this indicates the locale matching bug is present"
        )
