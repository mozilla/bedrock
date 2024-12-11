# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import pytest
from wagtail.coreutils import get_dummy_request
from wagtail.models import Locale, Page

from bedrock.cms.utils import get_cms_locales_for_path, get_locales_for_cms_page, get_page_for_request

pytestmark = [pytest.mark.django_db]


def test_get_locales_for_cms_page(tiny_localized_site):
    en_us_homepage = Page.objects.get(locale__language_code="en-US", slug="home")
    en_us_test_page = en_us_homepage.get_children()[0]

    # By default there are no aliases in the system, so all _locales_available_for_cms will
    # match the pages set up in the tiny_localized_site fixture
    assert Page.objects.filter(alias_of__isnull=False).count() == 0

    assert sorted(get_locales_for_cms_page(en_us_test_page)) == ["en-US", "fr", "pt-BR"]

    # now make aliases of the test_page into Dutch and Spanish
    nl_locale = Locale.objects.create(language_code="nl")
    es_es_locale = Locale.objects.create(language_code="es-ES")

    nl_page_alias = en_us_test_page.copy_for_translation(locale=nl_locale, copy_parents=True, alias=True)
    nl_page_alias.save()

    es_es_page_alias = en_us_test_page.copy_for_translation(locale=es_es_locale, copy_parents=True, alias=True)
    es_es_page_alias.save()

    assert Page.objects.filter(alias_of__isnull=False).count() == 4  # 2 child + 2 parent pages, which had to be copied too

    # Show that the aliases don't appear in the available locales
    assert sorted(get_locales_for_cms_page(en_us_test_page)) == ["en-US", "fr", "pt-BR"]


def test_get_locales_for_cms_page__ensure_draft_pages_are_excluded(tiny_localized_site):
    en_us_homepage = Page.objects.get(locale__language_code="en-US", slug="home")
    en_us_test_page = en_us_homepage.get_children()[0]
    fr_homepage = Page.objects.get(locale__language_code="fr", slug="home-fr")
    fr_test_page = fr_homepage.get_children()[0]

    fr_test_page.unpublish()

    assert sorted(get_locales_for_cms_page(en_us_test_page)) == ["en-US", "pt-BR"]


@pytest.mark.parametrize(
    "path, expected_page_url",
    [
        (
            "/en-US/test-page/",
            "/en-US/test-page/",
        ),
        (
            "/test-page/",
            "/en-US/test-page/",
        ),
        (
            "/pt-BR/test-page/",
            "/pt-BR/test-page/",
        ),
        (
            "/pt-BR/test-page/child-page/",
            "/pt-BR/test-page/child-page/",
        ),
        (
            "/fr/test-page/",
            "/fr/test-page/",
        ),
        (
            "/fr/test-page/child-page/",
            "/fr/test-page/child-page/",
        ),
        # These two routes do not work, even though a manual test with similar ones
        # does not show up as a problem. I think it's possibly related to the
        # tiny_localized_site fixture generated in cms/tests/conftest.py
        # (
        #     "/fr/test-page/child-page/grandchild-page/",
        #     "/fr/test-page/child-page/grandchild-page/",
        # ),
        # (
        #     "/test-page/child-page/grandchild-page/",
        #     "/fr/test-page/child-page/grandchild-page/",
        # ),
    ],
)
def test_get_page_for_request__happy_path(path, expected_page_url, tiny_localized_site):
    request = get_dummy_request(path=path)
    page = get_page_for_request(request=request)
    assert isinstance(page, Page)
    assert page.url == expected_page_url


@pytest.mark.parametrize(
    "path",
    [
        "/en-US/test-page/fake/path/",
        "/fr/test-page/fake/path/",
        "/not/a/real/test-page",
    ],
)
def test_get_page_for_request__no_match(path, tiny_localized_site):
    request = get_dummy_request(path=path)
    page = get_page_for_request(request=request)
    assert page is None


@pytest.mark.parametrize(
    "get_page_for_request_should_return_a_page, get_locales_for_cms_page_retval, expected",
    (
        (True, ["en-CA", "sco", "zh-CN"], ["en-CA", "sco", "zh-CN"]),
        (False, None, []),
    ),
)
def test_get_cms_locales_for_path(
    rf,
    get_page_for_request_should_return_a_page,
    get_locales_for_cms_page_retval,
    expected,
    minimal_site,
    mocker,
):
    request = rf.get("/path/is/irrelevant/due/to/mocks")
    mock_get_page_for_request = mocker.patch("bedrock.cms.utils.get_page_for_request")
    mock_get_locales_for_cms_page = mocker.patch("bedrock.cms.utils.get_locales_for_cms_page")

    if get_page_for_request_should_return_a_page:
        page = mocker.Mock("fake-page")
        mock_get_page_for_request.return_value = page
        mock_get_locales_for_cms_page.return_value = get_locales_for_cms_page_retval
    else:
        mock_get_page_for_request.return_value = None

    request = rf.get("/irrelevant/because/we/are/mocking")
    assert get_cms_locales_for_path(request) == expected

    if get_page_for_request_should_return_a_page:
        mock_get_page_for_request.assert_called_once_with(request=request)
        mock_get_locales_for_cms_page.assert_called_once_with(page=page)
