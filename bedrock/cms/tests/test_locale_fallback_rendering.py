# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os

from django.conf import settings
from django.template import engines
from django.test import override_settings
from django.urls import path

import pytest

from bedrock.base.i18n import bedrock_i18n_patterns
from bedrock.urls import urlpatterns as bedrock_urlpatterns
from lib import l10n_utils

pytestmark = [pytest.mark.django_db]

TEST_TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")


def _hreflang_test_view(request):
    return l10n_utils.render(
        request,
        "test-hreflang.html",
        {"active_locales": ["en-US", "es-MX", "fr", "de"]},
    )


urlpatterns = (
    bedrock_i18n_patterns(
        path("test-hreflang/", _hreflang_test_view, name="test-hreflang"),
    )
    + bedrock_urlpatterns
)


@pytest.fixture()
def _add_test_templates_dir():
    """Temporarily prepend the test templates directory to the Jinja2 searchpath.

    Modifies the loader's searchpath directly instead of resetting engines._engines,
    which would invalidate module-level references to the Jinja2 environment used by
    other tests' mock patches.
    """
    jinja2_loader = engines["jinja2"].env.loader
    jinja2_loader.searchpath.insert(0, TEST_TEMPLATES_DIR)
    try:
        yield
    finally:
        jinja2_loader.searchpath.remove(TEST_TEMPLATES_DIR)


@pytest.mark.urls(__name__)
@pytest.mark.usefixtures("_add_test_templates_dir")
@override_settings(FALLBACK_LOCALES={"es-AR": "es-MX", "es-CL": "es-MX"})
def test_non_cms_page_hreflang_alternates(client):
    """
    Non-CMS (Django/Fluent) pages render correct hreflang alternates.

    Uses a test-only view with controlled active_locales. Alias locales whose
    fallback is in active_locales must not appear in hreflang. Verifies from
    three perspectives: canonical locale, fallback target, and alias locale.
    """
    page_path = "/test-hreflang/"

    # --- 1. Canonical locale (en-US) ---
    response = client.get(f"/en-US{page_path}")
    assert response.status_code == 200
    html = response.text
    # The page is indexable
    assert 'content="noindex,follow"' not in html
    # The page is the canonical link.
    assert f'rel="canonical" href="{settings.CANONICAL_URL}/en-US{page_path}"' in html
    # The supported languages have hreflang entries.
    assert f'hreflang="en" href="{settings.CANONICAL_URL}/en-US{page_path}"' in html
    assert f'hreflang="es-MX" href="{settings.CANONICAL_URL}/es-MX{page_path}"' in html
    # The alias languages do not have a hreflang entries.
    assert 'hreflang="es-AR"' not in html
    assert 'hreflang="es-CL"' not in html

    # --- 2. Fallback target (es-MX, has content in active_locales) ---
    response = client.get(f"/es-MX{page_path}")
    assert response.status_code == 200
    html = response.text
    # The page is indexable
    assert 'content="noindex,follow"' not in html
    # The page is the canonical link.
    assert f'rel="canonical" href="{settings.CANONICAL_URL}/es-MX{page_path}"' in html
    # The supported languages have hreflang entries.
    assert f'hreflang="en" href="{settings.CANONICAL_URL}/en-US{page_path}"' in html
    assert f'hreflang="es-MX" href="{settings.CANONICAL_URL}/es-MX{page_path}"' in html
    # The alias languages do not have a hreflang entries.
    assert 'hreflang="es-AR"' not in html
    assert 'hreflang="es-CL"' not in html

    # --- 3. Alias locale (es-AR) served via non-CMS fallback ---
    response = client.get(f"/es-AR{page_path}")
    assert response.status_code == 200
    html = response.text
    # The page is not indexable
    assert 'content="noindex,follow"' in html
    # The page has a canonical link pointing to the es-MX page
    assert f'rel="canonical" href="{settings.CANONICAL_URL}/es-MX{page_path}"' in html
    assert f'rel="canonical" href="{settings.CANONICAL_URL}/es-AR{page_path}"' not in html
    # The alias languages do not have a hreflang entries.
    assert 'hreflang="es-AR"' not in html
    assert 'hreflang="es-CL"' not in html
