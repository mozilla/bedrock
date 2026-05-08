# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

pytestmark = pytest.mark.django_db


def test_about_this_site_has_canonical_and_noindex(client):
    # Representative of the most common noindex pattern: static pages that carry
    # `noindex,follow`. about/this-site.html is a simple static view with
    # no auth requirements.
    response = client.get("/en-US/about/this-site/")
    assert response.status_code == 200
    assert 'rel="canonical"' in response.text
    assert 'content="noindex,follow"' in response.text
    assert "/en-US/about/this-site/" in response.text


def test_vpn_mac_download_has_canonical_and_noindex_nofollow(client):
    # VPN download pages use `noindex,nofollow` (stricter than the common pattern)
    # and need the canonical link added directly rather than via a shared include,
    # because the shared include always emits `noindex,follow`.
    response = client.get("/en-US/products/vpn/download/mac/thanks/")
    assert response.status_code == 200
    assert 'rel="canonical"' in response.text
    assert 'content="noindex,nofollow"' in response.text


def test_newsletter_opt_out_has_canonical_and_noindex(client):
    # opt-out-confirmation.html uses bare `noindex` (no follow directive).
    # Asserts the robots value is exactly `noindex` and not inadvertently
    # changed to `noindex,follow` by the fix.
    response = client.get("/en-US/newsletter/opt-out-confirmation/")
    assert response.status_code == 200
    assert 'rel="canonical"' in response.text
    assert 'content="noindex"' in response.text
    assert 'content="noindex,follow"' not in response.text


def test_firefox_all_child_page_has_canonical_and_robots_none(client):
    # firefox/all/base.html uses a conditional block: when a product slug is
    # present in the URL path, it renders `content="none"`. The product slug
    # comes from the URL path, not a query parameter, so
    # /firefox/all/desktop-release/ triggers the branch.
    response = client.get("/en-US/firefox/all/desktop-release/")
    assert response.status_code == 200
    assert 'rel="canonical"' in response.text
    assert 'content="none"' in response.text


def test_whatsnew_new_theme_has_canonical_and_noindex(client):
    # whatsnew/base-new-theme.html is a standalone template that does not extend
    # base-protocol.html and has no canonical_urls block. The noindex meta and
    # canonical link are hardcoded directly in the <head>. Version 144.x routes
    # to whatsnew-fx144.html (extends base-new-theme.html) for en-US.
    response = client.get("/en-US/firefox/144.0/whatsnew/")
    assert response.status_code == 200
    assert 'rel="canonical"' in response.text
    assert 'content="noindex,follow"' in response.text


def test_normal_page_has_canonical_and_no_noindex(client):
    # Regression guard: a standard indexable static page must not gain a noindex
    # meta as a side effect of these changes.
    response = client.get("/en-US/about/manifesto/")
    assert response.status_code == 200
    assert 'rel="canonical"' in response.text
    assert 'content="noindex,follow"' not in response.text
