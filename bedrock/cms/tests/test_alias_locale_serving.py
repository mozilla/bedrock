# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.test.utils import override_settings

import pytest
from wagtail.models import Page, Site

from bedrock.cms.tests.factories import LocaleFactory

pytestmark = [pytest.mark.django_db]

ALIAS_SETTINGS = {
    "FALLBACK_LOCALES": {
        "pt-PT": "pt-BR",
        "en-GB": "en-US",
    }
}


@pytest.fixture
def localized_site_with_alias(tiny_localized_site):
    """
    Extends tiny_localized_site with a non-live pt-PT root page.

    Uses .copy() rather than .copy_for_translation() since copy_for_translation()
    walks up the tree and requires the Wagtail root (depth 1) to already have a
    pt-PT translation, which it never does. .copy() places the page directly
    without that parent check.
    """
    pt_pt_locale = LocaleFactory(language_code="pt-PT")

    en_us_locale_root = Page.objects.filter(
        depth=2,
        locale__language_code="en-US",
    ).first()
    wagtail_root = en_us_locale_root.get_parent()

    en_us_locale_root.copy(
        to=wagtail_root,
        update_attrs={
            "locale": pt_pt_locale,
            "slug": "home-pt-PT",
        },
        copy_revisions=False,
        keep_live=False,
        reset_translation_key=False,
        log_action=None,
    )

    return tiny_localized_site


@pytest.fixture
def site_with_es_es_and_aliases(tiny_localized_site):
    """
    Extends tiny_localized_site with:
    - es-ES: real translated content (test-page + child-page)
    - es-AR, es-CL: alias locales with non-live root pages only (no child-page)

    Uses copy_for_translation(copy_parents=True) for es-ES so the depth-2 site
    root is also translated. Uses .copy() for the alias locale roots for the same
    reason as the migration: copy_for_translation walks up to depth 1 and fails
    unless every ancestor is already translated.
    """
    site = Site.objects.get(is_default_site=True)
    en_us_root = site.root_page
    en_us_test_page = en_us_root.get_children()[0]
    en_us_child = Page.objects.get(locale__language_code="en-US", slug="child-page")
    wagtail_root = en_us_root.get_parent()

    es_es_locale = LocaleFactory(language_code="es-ES")
    es_es_test_page = en_us_test_page.copy_for_translation(es_es_locale, copy_parents=True)
    es_es_test_page.save_revision().publish()
    es_es_child = en_us_child.copy_for_translation(es_es_locale)
    es_es_child.save_revision().publish()

    for lang_code in ("es-AR", "es-CL"):
        alias_locale = LocaleFactory(language_code=lang_code)
        en_us_root.copy(
            to=wagtail_root,
            update_attrs={"locale": alias_locale, "slug": f"home-{lang_code}"},
            copy_revisions=False,
            keep_live=False,
            reset_translation_key=False,
            log_action=None,
        )

    return tiny_localized_site


@override_settings(**ALIAS_SETTINGS)
def test_cms_alias_locale_served_transparently(localized_site_with_alias, client):
    """GET /pt-PT/test-page/ returns 200 with pt-BR content, no redirect."""
    pt_br_page = Page.objects.get(locale__language_code="pt-BR", slug="test-page")
    # The "test-page" does not exist in the pt-PT locale.
    assert Page.objects.filter(locale__language_code="pt-PT", slug="test-page").exists() is False

    response = client.get("/pt-PT/test-page/", follow=False)

    assert response.status_code == 200
    assert pt_br_page.title in response.text
    # request.content_locale is set to the fallback locale code when serving an alias
    assert response.wsgi_request.content_locale == "pt-BR"


@override_settings(**ALIAS_SETTINGS)
def test_cms_alias_sets_locales_on_request(localized_site_with_alias, client):
    assert Page.objects.filter(locale__language_code="pt-BR", slug="test-page").exists() is True
    # The "test-page" does not exist in the pt-PT locale.
    assert Page.objects.filter(locale__language_code="pt-PT", slug="test-page").exists() is False

    response = client.get("/pt-PT/test-page/")

    assert response.status_code == 200
    # Both pt-PT and pt-BR are in _locales_available_via_cms.
    assert "pt-PT" in response.wsgi_request._locales_available_via_cms
    assert "pt-BR" in response.wsgi_request._locales_available_via_cms
    # The alias locale is not a content locale.
    assert "pt-PT" not in response.wsgi_request._content_locales_via_cms
    # The fallback locale is a content locale (since the page exists).
    assert "pt-BR" in response.wsgi_request._content_locales_via_cms


@override_settings(**ALIAS_SETTINGS)
def test_cms_alias_no_page_returns_404(localized_site_with_alias, client):
    """GET /pt-PT/nonexistent/ returns 404 when there is no matching pt-BR page."""
    assert Page.objects.filter(locale__language_code="pt-PT", slug="nonexistent").exists() is False
    assert Page.objects.filter(locale__language_code="pt-BR", slug="nonexistent").exists() is False

    response = client.get("/pt-PT/nonexistent/")

    assert response.status_code == 404


@override_settings(**ALIAS_SETTINGS)
def test_cms_alias_canonical_url_uses_fallback_locale(localized_site_with_alias, client):
    """The canonical <link> on an alias-served page points to the fallback locale URL."""
    assert Page.objects.filter(locale__language_code="pt-BR", slug="test-page").exists() is True
    # The "test-page" does not exist in the pt-PT locale.
    assert Page.objects.filter(locale__language_code="pt-PT", slug="test-page").exists() is False

    response = client.get("/pt-PT/test-page/")

    assert response.status_code == 200
    assert 'rel="canonical"' in response.text
    # The pt-PT URL must NOT appear as the canonical href
    canonical_line = [line for line in response.text.splitlines() if 'rel="canonical"' in line][0]
    assert "/pt-PT/" not in canonical_line
    # The pt-BR does appear as the canonical href
    assert "/pt-BR/" in canonical_line


@override_settings(**ALIAS_SETTINGS)
def test_cms_alias_noindex_present(localized_site_with_alias, client):
    """Alias-served pages carry noindex,follow robots meta."""
    assert Page.objects.filter(locale__language_code="pt-BR", slug="test-page").exists() is True
    # The "test-page" does not exist in the pt-PT locale.
    assert Page.objects.filter(locale__language_code="pt-PT", slug="test-page").exists() is False

    response = client.get("/pt-PT/test-page/")

    assert response.status_code == 200
    assert 'content="noindex,follow"' in response.text


@override_settings(**ALIAS_SETTINGS)
def test_cms_non_alias_no_noindex(localized_site_with_alias, client):
    """A normal (non-alias) page does NOT carry the noindex meta."""
    assert Page.objects.filter(locale__language_code="pt-BR", slug="test-page").exists() is True

    response = client.get("/pt-BR/test-page/")

    assert response.status_code == 200
    assert 'content="noindex,follow"' not in response.text


@override_settings(**ALIAS_SETTINGS)
def test_cms_alias_hreflang_excludes_alias_locale(localized_site_with_alias, client):
    """
    Alias locales without their own content are excluded from hreflang output.
    pt-PT has no translated content in this fixture, so it should not appear.
    """
    assert Page.objects.filter(locale__language_code="pt-BR", slug="test-page").exists() is True
    # The "test-page" does not exist in the pt-PT locale.
    assert Page.objects.filter(locale__language_code="pt-PT", slug="test-page").exists() is False

    response = client.get("/pt-PT/test-page/")

    assert response.status_code == 200
    assert 'hreflang="pt-PT"' not in response.text


@override_settings(**ALIAS_SETTINGS)
def test_cms_hreflang_pt_br_claims_bare_pt(localized_site_with_alias, client):
    """
    The pt-BR page claims hreflang='pt' (bare) now that pt-PT is an alias.
    Verify from a pt-BR page (the content locale URL).
    """
    assert Page.objects.filter(locale__language_code="pt-BR", slug="test-page").exists() is True

    response = client.get("/pt-BR/test-page/")

    assert response.status_code == 200
    assert 'hreflang="pt"' in response.text
    bare_pt_line = [line for line in response.text.splitlines() if 'hreflang="pt"' in line][0]
    assert "/pt-BR/" in bare_pt_line  # bare "pt" points to pt-BR, not pt-PT


@override_settings(FALLBACK_LOCALES={"es-AR": "es-ES", "es-CL": "es-ES"})
def test_cms_alias_locales_excluded_from_hreflang_on_all_pages(site_with_es_es_and_aliases, client):
    """
    Alias locales without their own content are excluded from hreflang on every page:
    the canonical locale, the fallback target, and the alias page itself.
    """
    page_path = "/test-page/child-page/"
    en_us_child = Page.objects.get(locale__language_code="en-US", slug="child-page")
    es_es_child = Page.objects.get(locale__language_code="es-ES", slug="child-page")
    # The "child-page" does not exist in the es-AR or es-CL locales.
    assert Page.objects.filter(locale__language_code="es-AR", slug="child-page").exists() is False
    assert Page.objects.filter(locale__language_code="es-CL", slug="child-page").exists() is False

    # --- 1. Canonical locale (en-US) ---
    response = client.get(en_us_child.url)
    assert response.status_code == 200
    html = response.text
    assert f'rel="canonical" href="{settings.CANONICAL_URL}/en-US{page_path}"' in html
    assert 'content="noindex,follow"' not in html
    assert 'hreflang="es-ES"' in html
    assert 'hreflang="es-AR"' not in html
    assert 'hreflang="es-CL"' not in html

    # --- 2. Fallback target (es-ES, has real content) ---
    es_es_child.refresh_from_db()
    response = client.get(es_es_child.url)
    assert response.status_code == 200
    html = response.text
    assert f'rel="canonical" href="{settings.CANONICAL_URL}/es-ES{page_path}"' in html
    assert 'content="noindex,follow"' not in html
    assert 'hreflang="es-AR"' not in html
    assert 'hreflang="es-CL"' not in html

    # --- 3. Alias locale (es-AR) served via fallback ---
    es_ar_url = es_es_child.url.replace("es-ES", "es-AR")
    response = client.get(es_ar_url)
    assert response.status_code == 200
    html = response.text
    assert f'rel="canonical" href="{settings.CANONICAL_URL}/es-ES{page_path}"' in html
    assert f'rel="canonical" href="{settings.CANONICAL_URL}/es-AR{page_path}"' not in html
    assert 'content="noindex,follow"' in html
    assert 'hreflang="es-ES"' in html
    assert 'hreflang="es-AR"' not in html
    assert 'hreflang="es-CL"' not in html


@override_settings(**ALIAS_SETTINGS)
def test_cms_promoted_alias_locale_included_in_hreflang(tiny_localized_site, client):
    """
    When an alias locale has its own translated content ('promoted'), it appears
    in hreflang alternates like any other real locale.
    """
    site = Site.objects.get(is_default_site=True)
    en_us_root = site.root_page
    en_us_test_page = en_us_root.get_children()[0]
    en_us_child = Page.objects.get(locale__language_code="en-US", slug="child-page")

    pt_pt_locale = LocaleFactory(language_code="pt-PT")
    pt_pt_root = en_us_root.copy_for_translation(pt_pt_locale)
    pt_pt_root.live = True
    pt_pt_root.save()
    pt_pt_test_page = en_us_test_page.copy_for_translation(pt_pt_locale)
    pt_pt_test_page.save_revision().publish()
    pt_pt_child = en_us_child.copy_for_translation(pt_pt_locale)
    pt_pt_child.save_revision().publish()

    page_path = "/test-page/child-page/"
    pt_br_child = Page.objects.get(locale__language_code="pt-BR", slug="child-page")

    response_pt_br = client.get(pt_br_child.url)

    assert response_pt_br.status_code == 200
    html = response_pt_br.text
    # Both pt-BR and pt-PT have their own content — both must appear.
    assert f'hreflang="pt-BR" href="{settings.CANONICAL_URL}/pt-BR{page_path}"' in html
    assert f'hreflang="pt-PT" href="{settings.CANONICAL_URL}/pt-PT{page_path}"' in html
    assert 'content="noindex,follow"' not in html

    response_pt_pt = client.get(pt_pt_child.url)

    assert response_pt_pt.status_code == 200
    html = response_pt_pt.text
    # Both pt-BR and pt-PT have their own content — both must appear.
    assert f'hreflang="pt-BR" href="{settings.CANONICAL_URL}/pt-BR{page_path}"' in html
    assert f'hreflang="pt-PT" href="{settings.CANONICAL_URL}/pt-PT{page_path}"' in html
    assert 'content="noindex,follow"' not in html
