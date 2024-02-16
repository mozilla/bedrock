# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest
import requests
from redirects.base import assert_valid_url


@pytest.mark.headless
@pytest.mark.nondestructive
@pytest.mark.parametrize(
    "url",
    [
        "privacy/",
        "privacy/firefox/",
        "privacy/firefox-focus/",
        "privacy/subscription-services/",
    ],
)
def test_privacy_policies_always_200_OK(
    url,
    base_url,
):
    """Smoke test to ensure that our privacy pages always
    ultimately return a 200 OK response, even if the client
    requesting them lacks an Accept-Language header and there
    is no locale in the actual URL
    """

    # A loop in a parametrized test isn't great, but it does make the `url`
    # options simpler to grok and to extend
    for url, accept_language_header in [
        (f"/{url}", None),
        (f"/{url}", "*"),
        (f"/{url}", "de"),
        (f"/{url}", "br-PT"),
        (f"/en-US/{url}", None),
        (f"/en-US/{url}", "*"),
        (f"/en-US/{url}/", "de"),
        (f"/en-US/{url}/", "br-PT"),
    ]:
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
