# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest
import requests

TIMEOUT = 60


def pytest_generate_tests(metafunc):
    if "not headless" in metafunc.config.option.markexpr:
        return  # test deslected by mark expression
    base_url = metafunc.config.option.base_url
    if not base_url:
        pytest.skip("This test requires a base URL to be specified on the command line or in a configuration file.")
    paths = (
        "/about/forums/",
        "/about/legal/",
        "/about/legal/terms/mozilla/",
        "/about/legal/terms/services/",
        "/about/legal/terms/firefox-hello/",
        "/about/legal/terms/firefox/",
        "/about/legal/terms/thunderbird/",
        "/credits/",
        "/privacy/",
        "/privacy/principles/",
        "/privacy/websites/",
        "/privacy/firefox/",
        "/privacy/firefox-os/",
        "/privacy/firefox-cloud/",
        "/privacy/thunderbird/",
        "/security/",
        "/security/advisories/",
        "/security/known-vulnerabilities/",
        "/security/known-vulnerabilities/firefox/",
        "/security/known-vulnerabilities/firefox-esr/",
        "/security/known-vulnerabilities/firefox-os/",
        "/security/known-vulnerabilities/thunderbird/",
        "/security/known-vulnerabilities/thunderbird-esr/",
        "/security/known-vulnerabilities/seamonkey/",
        "/security/known-vulnerabilities/firefox-3.6/",
        "/security/known-vulnerabilities/firefox-3.5/",
        "/security/known-vulnerabilities/firefox-3.0/",
        "/security/known-vulnerabilities/firefox-2.0/",
        "/security/known-vulnerabilities/firefox-1.5/",
        "/security/known-vulnerabilities/firefox-1.0/",
        "/security/known-vulnerabilities/thunderbird-3.1/",
        "/security/known-vulnerabilities/thunderbird-3.0/",
        "/security/known-vulnerabilities/thunderbird-2.0/",
        "/security/known-vulnerabilities/thunderbird-1.5/",
        "/security/known-vulnerabilities/thunderbird-1.0/",
        "/security/known-vulnerabilities/seamonkey-2.0/",
        "/security/known-vulnerabilities/seamonkey-1.1/",
        "/security/known-vulnerabilities/seamonkey-1.0/",
        "/security/known-vulnerabilities/mozilla-suite/",
        "/security/known-vulnerabilities/older-vulnerabilities/",
    )
    metafunc.parametrize("url", [base_url + path for path in paths])


@pytest.mark.headless
@pytest.mark.nondestructive
def test_generated_pages(url):
    r = requests.head(url, allow_redirects=True, timeout=TIMEOUT, headers={"accept-language": "en"})
    assert requests.codes.ok == r.status_code
