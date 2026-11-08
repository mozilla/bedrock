# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import requests
from pyquery import PyQuery as pq

TIMEOUT = 60


def pytest_generate_tests(metafunc):
    markexpr = metafunc.config.getoption("markexpr")
    if markexpr == "download":
        base_url = metafunc.config.getoption("base_url")
        if "download_path" in metafunc.fixturenames:
            doc = get_web_page(f"{base_url}/en-US/firefox/download/thanks/")
            urls = [a.attrib["href"] for a in doc("ul.download-list a")]
            # Bug 1266682 remove links to Play Store to avoid rate limiting in automation.
            skip_urls = ["https://play.google.com", "https://apps.apple.com"]
            urls = list(filter(lambda url: not any([s in url for s in skip_urls]), urls))
            assert urls
            metafunc.parametrize("download_path", urls)


def get_web_page(url):
    try:
        r = requests.get(url, timeout=TIMEOUT, headers={"accept-language": "en"})
    except requests.RequestException:
        # retry
        r = requests.get(url, timeout=TIMEOUT, headers={"accept-language": "en"})
    return pq(r.content)
