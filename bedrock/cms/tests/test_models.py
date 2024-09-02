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
from bedrock.cms.tests.factories import StructuralPageFactory

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


def test__patch_request_for_bedrock__locales_available_via_cms(tiny_localized_site, rf):
    request = rf.get("/some-path/that/is/irrelevant")
    en_us_homepage = Page.objects.get(locale__language_code="en-US", slug="home")
    en_us_test_page = en_us_homepage.get_children()[0]

    # By default there are no aliases in the system, so all _locales_available_for_cms will
    # match the pages set up in the tiny_localized_site fixture
    assert Page.objects.filter(alias_of__isnull=False).count() == 0

    patched_request = en_us_test_page.specific._patch_request_for_bedrock(request)
    assert sorted(patched_request._locales_available_via_cms) == ["en-US", "fr", "pt-BR"]

    # now make aliases of the test_page into Dutch and Spanish
    nl_locale = Locale.objects.create(language_code="nl")
    es_es_locale = Locale.objects.create(language_code="es-ES")

    nl_page_alias = en_us_test_page.copy_for_translation(locale=nl_locale, copy_parents=True, alias=True)
    nl_page_alias.save()

    es_es_page_alias = en_us_test_page.copy_for_translation(locale=es_es_locale, copy_parents=True, alias=True)
    es_es_page_alias.save()

    assert Page.objects.filter(alias_of__isnull=False).count() == 4  # 2 child + 2 parent pages, which had to be copied too

    # Show that the aliases don't appear in the available locales
    patched_request = en_us_test_page.specific._patch_request_for_bedrock(request)
    assert sorted(patched_request._locales_available_via_cms) == ["en-US", "fr", "pt-BR"]


def test__patch_request_for_bedrock_annotates_is_cms_page(tiny_localized_site, rf):
    request = rf.get("/some-path/that/is/irrelevant")
    en_us_homepage = Page.objects.get(locale__language_code="en-US", slug="home")
    en_us_test_page = en_us_homepage.get_children()[0]
    assert en_us_test_page.specific.__class__ == SimpleRichTextPage

    patched_request = en_us_test_page.specific._patch_request_for_bedrock(request)
    assert patched_request.is_cms_page is True
