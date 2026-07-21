# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import patch

import pytest
from wagtail.models import Locale, Page, PageViewRestriction, Site

from bedrock.anonym.models import AnonymNewsItemPage, AnonymNewsPage
from bedrock.cms.tests.factories import LocaleFactory, SimpleRichTextPageFactory, StructuralPageFactory
from bedrock.sitemaps.utils import (
    _path_for_cms_url,
    get_wagtail_urls,
    update_sitemaps,
)

pytestmark = pytest.mark.django_db


@pytest.fixture
def dummy_wagtail_pages():
    en_us_locale = Locale.objects.get(language_code="en-US")
    fr_locale = LocaleFactory(language_code="fr")
    pt_br_locale = LocaleFactory(language_code="pt-BR")

    site = Site.objects.get(is_default_site=True)

    en_us_root_page = site.root_page
    fr_root_page = en_us_root_page.copy_for_translation(fr_locale)
    pt_br_root_page = en_us_root_page.copy_for_translation(pt_br_locale)

    en_us_structural_page = StructuralPageFactory(
        title="Structural test page",
        slug="test-structural-page",
        parent=en_us_root_page,
    )
    en_us_child_of_structural = SimpleRichTextPageFactory(
        title="Child of structural",
        slug="structural-sub-child",
        parent=en_us_structural_page,
    )

    en_us_page = SimpleRichTextPageFactory(title="Test Page", slug="test-page", parent=en_us_root_page)

    fr_page = en_us_page.copy_for_translation(fr_locale)
    fr_page.title = "Page de Test"
    fr_page.save()
    rev = fr_page.save_revision()
    fr_page.publish(rev)

    fr_child = SimpleRichTextPageFactory(
        title="Enfant",
        slug="child-page",
        parent=fr_page,
    )
    fr_grandchild = SimpleRichTextPageFactory(
        title="Petit-enfant",
        slug="grandchild-page",
        parent=fr_child,
    )

    pt_br_page = en_us_page.copy_for_translation(pt_br_locale)
    pt_br_page.title = "Página de Teste"
    pt_br_page.save()
    rev = pt_br_page.save_revision()
    pt_br_page.publish(rev)

    pt_br_child = fr_child.copy_for_translation(pt_br_locale)
    pt_br_child.title = "Página Filho"
    pt_br_child.save()
    rev = pt_br_child.save_revision()
    pt_br_child.publish(rev)

    assert en_us_root_page.locale == en_us_locale
    assert pt_br_root_page.locale == pt_br_locale
    assert fr_root_page.locale == fr_locale

    assert en_us_structural_page.locale == en_us_locale
    assert en_us_child_of_structural.locale == en_us_locale
    assert en_us_page.locale == en_us_locale
    assert pt_br_page.locale == pt_br_locale
    assert pt_br_child.locale == pt_br_locale
    assert fr_page.locale == fr_locale
    assert fr_child.locale == fr_locale
    assert fr_grandchild.locale == fr_locale

    for page in (
        en_us_page,
        en_us_structural_page,
        en_us_child_of_structural,
        pt_br_page,
        pt_br_child,
        fr_page,
        fr_child,
        fr_grandchild,
    ):
        page.refresh_from_db()

    assert en_us_page.live is True
    assert en_us_structural_page.live is True
    assert en_us_child_of_structural.live is True
    assert pt_br_page.live is True
    assert pt_br_child.live is True
    assert fr_page.live is True
    assert fr_child.live is True
    assert fr_grandchild.live is True


def test_get_wagtail_urls(dummy_wagtail_pages):
    urls = get_wagtail_urls()

    # Initially, all the pages set up in `dummy_wagtail_pages` are available, unless
    # they are StructuralPages - but note that children of StructuralPages _must_ be included
    assert urls == {
        "/test-structural-page/structural-sub-child/": ["en-US"],
        "/test-page/": ["en-US", "fr", "pt-BR"],
        "/test-page/child-page/": ["fr", "pt-BR"],
        "/test-page/child-page/grandchild-page/": ["fr"],
    }

    # Now unpublish one and confirm that it's not included
    pt_br_child = Page.objects.get(locale__language_code="pt-BR", slug="child-page")
    pt_br_child.unpublish()
    pt_br_child.save()

    urls = get_wagtail_urls()
    assert urls == {
        "/test-structural-page/structural-sub-child/": ["en-US"],
        "/test-page/": ["en-US", "fr", "pt-BR"],
        "/test-page/child-page/": ["fr"],
        "/test-page/child-page/grandchild-page/": ["fr"],
    }

    # Now make one private and confirm that it is also exlcuded
    fr_grandchild = Page.objects.get(locale__language_code="fr", slug="grandchild-page")
    PageViewRestriction.objects.create(
        page=fr_grandchild,
        restriction_type=PageViewRestriction.PASSWORD,
        password="secretpassword",
    )
    urls = get_wagtail_urls()
    assert urls == {
        "/test-structural-page/structural-sub-child/": ["en-US"],
        "/test-page/": ["en-US", "fr", "pt-BR"],
        "/test-page/child-page/": ["fr"],
    }

    # Now unpublish the child of the structural page and it should disappear, along with
    # the parent (test-structural-page) route
    en_structural_child = Page.objects.get(locale__language_code="en-US", slug="structural-sub-child")
    en_structural_child.unpublish()
    en_structural_child.save()
    urls = get_wagtail_urls()
    assert urls == {
        "/test-page/": ["en-US", "fr", "pt-BR"],
        "/test-page/child-page/": ["fr"],
    }


def test_get_wagtail_urls__exclude_from_sitemap(dummy_wagtail_pages):
    """Test that pages with exclude_from_sitemap=True are excluded from sitemap."""
    site = Site.objects.get(is_default_site=True)
    en_us_root_page = site.root_page

    # Create an AnonymNewsPage
    news_page = AnonymNewsPage(
        title="News",
        slug="news",
        live=True,
    )
    en_us_root_page.add_child(instance=news_page)
    news_page.save_revision().publish()

    # Create a news item without external link (should be included)
    news_item_without_link = AnonymNewsItemPage(
        title="Internal News Item",
        slug="internal-news",
        live=True,
        link="",  # No external link
    )
    news_page.add_child(instance=news_item_without_link)
    news_item_without_link.save_revision().publish()

    # Create a news item with external link (should be excluded)
    news_item_with_link = AnonymNewsItemPage(
        title="External News Item",
        slug="external-news",
        live=True,
        link="https://example.com/article",  # Has external link
    )
    news_page.add_child(instance=news_item_with_link)
    news_item_with_link.save_revision().publish()

    urls = get_wagtail_urls()

    # The news page and news item without link should be included
    assert "/news/" in urls
    assert "/news/internal-news/" in urls

    # The news item with external link should be excluded
    assert "/news/external-news/" not in urls


@pytest.mark.parametrize(
    "page_url, lang_code, expected",
    (
        (
            # expected behaviour: strip the locale and leading slash
            "/fr/some/path/here/fr/",
            "fr",
            "/some/path/here/fr/",
        ),
        (
            # only strip the locale and leading slash if it's for the given lang code
            "/some/path/here/fr/",
            "fr",
            "/some/path/here/fr/",
        ),
        (
            # confirm region-based locales also work
            "/en-US/some/path/here/en-US/",
            "en-US",
            "/some/path/here/en-US/",
        ),
        (
            # show we definitely only replace one, the first
            # 6 in input; 5 output
            "/de/de/de/de/de/de/",
            "de",
            "/de/de/de/de/de/",
        ),
        (
            # root path for a locale
            "/it/",
            "it",
            "/",
        ),
        (
            # unrealistic, but proves the point that we only replace the locale code if the given lang code matches
            "/fr/some/path/here/fr/",
            "de",
            "/fr/some/path/here/fr/",
        ),
    ),
)
def test_path_for_cms_url(page_url, lang_code, expected):
    # General test for Issue #15805
    assert _path_for_cms_url(page_url, lang_code) == expected


def test_get_wagtail_urls__ensure_locale_codes_not_stripped(dummy_wagtail_pages):
    # Focused test for Issue #15805
    fr_test_child_page = Page.objects.get(slug="child-page", locale__language_code="fr")
    fr_test_child_page.slug = f"fr-{fr_test_child_page.slug}fr"
    fr_test_child_page.save()

    fr_test_child_page.refresh_from_db()
    assert fr_test_child_page.slug == "fr-child-pagefr"
    assert fr_test_child_page.url == "/fr/test-page/fr-child-pagefr/"

    urls = get_wagtail_urls()
    assert urls["/test-page/fr-child-pagefr/"] == ["fr"]


@patch("bedrock.sitemaps.utils.get_static_urls")
@patch("bedrock.sitemaps.utils.get_security_urls")
@patch("bedrock.sitemaps.utils.get_wagtail_urls")
@patch("bedrock.sitemaps.utils.output_json")
def test_update_sitemaps(
    mock_output_json,
    mock_get_wagtail_urls,
    mock_get_security_urls,
    mock_get_static_urls,
):
    "Light check to ensure we've not added _new_ things we haven't added tests for"

    mock_get_wagtail_urls.return_value = {"wagtail": "walterite"}
    mock_get_security_urls.return_value = {"security": "grainwave"}
    mock_get_static_urls.return_value = {"static_urls": "rubberduck"}

    update_sitemaps()
    expected = {
        "wagtail": "walterite",
        "security": "grainwave",
        "static_urls": "rubberduck",
    }

    mock_output_json.assert_called_once_with(expected)
