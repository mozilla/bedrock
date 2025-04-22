# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Test the way Wagtail pages are handled by lib.l10n_utils.render

# The pytest fixtures used to run these tests are defined in bedrock/cms/tests/conftest.py

from django.conf import settings

import pytest
from wagtail.models import Locale, Page

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
