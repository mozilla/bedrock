# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest import mock

from django.test import override_settings

import pytest
from wagtail.models import Locale, Page

from bedrock.cms.models import (
    AbstractBedrockCMSPage,
    SimpleRichTextPage,
    StructuralPage,
)
from bedrock.cms.tests.factories import LocaleFactory, StructuralPageFactory

pytestmark = [
    pytest.mark.django_db,
]


@mock.patch("bedrock.cms.models.SimpleRichTextPage.get_view_restrictions")
@pytest.mark.parametrize(
    "fake_restrictions, expected_headers",
    (
        ([], "max-age=600"),
        ([mock.Mock()], "max-age=0, no-cache, no-store, must-revalidate, private"),
    ),
    ids=[
        "Default, unrestricted-page behaviour",
        "Restricted-page behaviour",
    ],
)
def test_cache_control_headers_on_pages_with_view_restrictions(
    mock_get_view_restrictions,
    fake_restrictions,
    expected_headers,
    client,
    minimal_site,
):
    mock_get_view_restrictions.return_value = fake_restrictions

    page = SimpleRichTextPage.objects.last()  # made by the minimal_site fixture

    # Confirm we're using the base page
    assert isinstance(page, AbstractBedrockCMSPage)

    _relative_url = page.relative_url(minimal_site)
    assert _relative_url == "/en-US/test-page/"

    response = client.get(_relative_url)

    assert response.get("Cache-Control") == expected_headers


def test_StructuralPage_serve_methods(
    minimal_site,
    rf,
):
    "Show that structural pages redirect to their parent rather than serve anything"

    root_page = SimpleRichTextPage.objects.first()
    sp = StructuralPageFactory(parent=root_page, slug="folder-page")
    sp.save()

    _relative_url = sp.relative_url(minimal_site)
    assert _relative_url == "/en-US/folder-page/"

    request = rf.get(_relative_url)
    live_result = sp.serve(request)
    assert live_result.headers["location"].endswith(root_page.url)

    preview_result = sp.serve_preview(request)
    assert preview_result.headers["location"].endswith(root_page.url)


@pytest.mark.parametrize(
    "config, page_class, success_expected",
    (
        ("__all__", SimpleRichTextPage, True),  # same as default
        ("mozorg.SomeOtherPageClass,cms.StructuralPage,cms.SimpleRichTextPage", StructuralPage, True),
        ("cms.SimpleRichTextPage", SimpleRichTextPage, True),
        ("cms.SimpleRichTextPage,mozorg.SomeOtherPageClass", SimpleRichTextPage, True),
        ("mozorg.SomeOtherPageClass,cms.SimpleRichTextPage", SimpleRichTextPage, True),
        ("mozorg.SomeOtherPageClass,mozorg.SomeOtherPageClass", SimpleRichTextPage, False),
        ("mozorg.SomeOtherPageClass", SimpleRichTextPage, False),
        ("mozorg.SomeOtherPageClass,legal.SomeLegalPageClass", StructuralPage, False),
    ),
)
def test_CMS_ALLOWED_PAGE_MODELS_controls_Page_can_create_at(
    config,
    page_class,
    success_expected,
    minimal_site,
):
    home_page = SimpleRichTextPage.objects.last()
    with override_settings(Dev=False, CMS_ALLOWED_PAGE_MODELS=config.split(",")):
        assert page_class.can_create_at(home_page) == success_expected


@mock.patch("bedrock.cms.models.base.get_locales_for_cms_page")
def test__patch_request_for_bedrock__locales_available_via_cms(
    mock_get_locales_for_cms_page,
    minimal_site,
    rf,
):
    request = rf.get("/some-path/that/is/irrelevant")

    page = SimpleRichTextPage.objects.last()  # made by the minimal_site fixture

    mock_get_locales_for_cms_page.return_value = ["en-US", "fr", "pt-BR"]

    patched_request = page.specific._patch_request_for_bedrock(request)
    assert sorted(patched_request._locales_available_via_cms) == ["en-US", "fr", "pt-BR"]


def test__patch_request_for_bedrock_annotates_is_cms_page(tiny_localized_site, rf):
    request = rf.get("/some-path/that/is/irrelevant")
    en_us_homepage = Page.objects.get(locale__language_code="en-US", slug="home")
    en_us_test_page = en_us_homepage.get_children()[0]
    assert en_us_test_page.specific.__class__ == SimpleRichTextPage

    patched_request = en_us_test_page.specific._patch_request_for_bedrock(request)
    assert patched_request.is_cms_page is True


@pytest.mark.parametrize(
    "django_locale,expected_locale_code",
    [
        ("en-gb", "en-GB"),  # Lowercase from Django -> mixed-case
        ("en-ca", "en-CA"),  # Another mixed-case example
        ("pt-br", "pt-BR"),  # Another mixed-case example
        ("es-es", "es-ES"),  # Another mixed-case example
        ("es-ar", "es-AR"),  # Another mixed-case example
        ("de", "de"),  # Simple code stays the same
    ],
)
def test_bedrock_locale_get_active_normalizes_case(django_locale, expected_locale_code):
    """
    Test that BedrockLocale.get_active() normalizes Django's lowercase
    language codes to match Bedrock's mixed-case Locale records.
    This is a unit test for the BedrockLocale.get_active() method that
    verifies it properly handles the case mismatch between Django's internal
    lowercase language codes (e.g., 'en-gb') and Bedrock's mixed-case
    Locale records (e.g., 'en-GB').
    Without this normalization, Wagtail's routing would fail to find the
    correct Locale and fall back to the default locale.
    """
    # Create the Locale record with mixed-case code
    locale = LocaleFactory(language_code=expected_locale_code)
    assert locale.language_code == expected_locale_code

    # Mock Django's translation.get_language() to return lowercase
    with mock.patch("django.utils.translation.get_language", return_value=django_locale):
        # Call BedrockLocale.get_active() (which is patched onto Locale)
        active_locale = Locale.get_active()

        # Verify it found the correct Locale despite the case mismatch
        assert active_locale.id == locale.id
        assert active_locale.language_code == expected_locale_code


def test_bedrock_locale_get_active_falls_back_to_default():
    """
    Test that BedrockLocale.get_active() falls back to the default locale
    when the requested locale doesn't exist.
    """
    # Ensure en-US exists as the default
    default_locale = Locale.objects.get(language_code="en-US")

    # Mock Django returning a locale that doesn't exist
    with mock.patch("django.utils.translation.get_language", return_value="xx-YY"):
        active_locale = Locale.get_active()

        # Should fall back to en-US
        assert active_locale.id == default_locale.id
        assert active_locale.language_code == "en-US"
