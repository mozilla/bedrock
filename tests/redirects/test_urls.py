# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""Test redirects from the global.conf file."""
import pytest
import requests

from .base import assert_valid_url
from .map_410 import URLS_410


@pytest.mark.headless
@pytest.mark.nondestructive
@pytest.mark.django_db
@pytest.mark.parametrize("url", URLS_410)
def test_410_url(url, base_url):
    assert_valid_url(url, base_url=base_url, status_code=requests.codes.gone)


@pytest.mark.headless
@pytest.mark.nondestructive
@pytest.mark.django_db
def test_404_url(base_url):
    assert_valid_url("/en-US/abck", status_code=requests.codes.not_found, base_url=base_url)


@pytest.mark.headless
@pytest.mark.nondestructive
@pytest.mark.django_db
@pytest.mark.parametrize(
    "url",
    [
        "/firefox/android/",
        "/firefox/android/faq/",
        "/firefox/brand/",
        "/firefox/channel/",
        "/firefox/desktop/",
        "/firefox/interest-dashboard/",
        "/firefox/mobile/",
        "/firefox/os/",
        "/firefox/os/notes/1.1/",
        "/firefox/partners/",
        "/firefox/speed/",
        "/firefox/tiles/",
        "/firefox/unsupported/EOL/",
        # Legacy URLs (Bug 1110927)
        "/firefox/start/central.html",
        "/firefox/sync/firstrun.html",
    ],
)
def test_301_urls(url, base_url, follow_redirects=False):
    assert_valid_url(url, base_url=base_url, follow_redirects=follow_redirects)


@pytest.mark.headless
@pytest.mark.nondestructive
@pytest.mark.django_db
@pytest.mark.parametrize(
    "url",
    [
        "/firefox/",
        "/firefox/all/",
        "/firefox/developer/",
        "/firefox/installer-help/",
        "/firefox/latest/releasenotes/",
        "/firefox/new/",
        "/firefox/nightly/firstrun/",
        "/firefox/releases/",
        "/firefox/unsupported-systems/",
    ],
)
def test_302_urls(url, base_url, follow_redirects=False):
    assert_valid_url(url, base_url=base_url, follow_redirects=follow_redirects, status_code=requests.codes.found)


@pytest.mark.headless
@pytest.mark.nondestructive
@pytest.mark.django_db
@pytest.mark.parametrize(
    "url,accept_language_header",
    [
        # Mozorg privacy
        ("/en-US/privacy/", None),
        ("/en-US/privacy/", "*"),
        ("/en-US/privacy/", "de"),
        ("/en-US/privacy/", "br-PT"),
        ("/privacy/", None),
        ("/privacy/", "*"),
        ("/privacy/", "de"),
        ("/privacy/", "br-PT"),
        # Fx privacy
        ("/en-US/privacy/firefox/", None),
        ("/en-US/privacy/firefox/", "*"),
        ("/en-US/privacy/firefox/", "de"),
        ("/en-US/privacy/firefox/", "br-PT"),
        ("/privacy/firefox/", None),
        ("/privacy/firefox/", "*"),
        ("/privacy/firefox/", "de"),
        ("/privacy/firefox/", "br-PT"),
        # Focus privacy
        ("/en-US/privacy/firefox-focus/", None),
        ("/en-US/privacy/firefox-focus/", "*"),
        ("/en-US/privacy/firefox-focus/", "de"),
        ("/en-US/privacy/firefox-focus/", "br-PT"),
        ("/privacy/firefox-focus/", None),
        ("/privacy/firefox-focus/", "*"),
        ("/privacy/firefox-focus/", "de"),
        ("/privacy/firefox-focus/", "br-PT"),
        # Mozilla VPN privacy
        ("/en-US/privacy/mozilla-vpn/", None),
        ("/en-US/privacy/mozilla-vpn/", "*"),
        ("/en-US/privacy/mozilla-vpn/", "de"),
        ("/en-US/privacy/mozilla-vpn/", "br-PT"),
        ("/privacy/mozilla-vpn/", None),
        ("/privacy/mozilla-vpn/", "*"),
        ("/privacy/mozilla-vpn/", "de"),
        ("/privacy/mozilla-vpn/", "br-PT"),
    ],
)
def test_privacy_policies_always_200_OK(
    url,
    base_url,
    accept_language_header,
):
    """Smoke test to ensure that our privacy pages always
    ultimately return a 200 OK response, even if the client
    requesting them lacks an Accept-Language header and there
    is no locale in the actual URL
    """

    req_headers = {}
    if accept_language_header:
        req_headers["Accept-Language"] = accept_language_header

    assert_valid_url(
        url,
        base_url=base_url,
        req_headers=req_headers,
        follow_redirects=True,
        final_status_code=requests.codes.ok,
    )


@pytest.mark.headless
@pytest.mark.nondestructive
@pytest.mark.django_db
@pytest.mark.parametrize(
    "url,accept_language_header",
    [
        # Klar privacy - DE only
        ("/de/privacy/firefox-klar/", None),
        ("/de/privacy/firefox-klar/", "*"),
        ("/de/privacy/firefox-klar/", "en-US"),
        ("/de/privacy/firefox-klar/", "br-PT"),
        ("/privacy/firefox-klar/", None),  # ends up on /en-US/firefox-focus
        ("/privacy/firefox-klar/", "*"),  # ends up on /en-US/firefox-focus
        ("/privacy/firefox-klar/", "en-US"),  # ends up on /en-US/firefox-focus
        ("/privacy/firefox-klar/", "br-PT"),  # ends up on /en-US/firefox-focus
    ],
)
def test_privacy_policies_always_200_OK__special_cases(
    url,
    base_url,
    accept_language_header,
):
    """Smoke test to ensure that our privacy pages always
    ultimately return a 200 OK response, even if the client
    requesting them lacks an Accept-Language header and there
    is no locale in the actual URL
    """

    req_headers = {}
    if accept_language_header:
        req_headers["Accept-Language"] = accept_language_header

    assert_valid_url(
        url,
        base_url=base_url,
        req_headers=req_headers,
        follow_redirects=True,
        final_status_code=requests.codes.ok,
    )
