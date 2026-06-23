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

        elif "download_path_l10n" in metafunc.fixturenames:
            urls = []
            doc = get_web_page(f"{base_url}/en-US/firefox/all/")
            product_urls = [a.attrib["href"] for a in doc("ul.c-product-list a")]
            # FIXME: sanity checks after first scene is redirected to FXC:
            if product_urls and product_urls[0].startswith("/en-US/download/all/"):
                product_urls = ["/en-US/firefox/all/desktop-release/", "/en-US/firefox/all/desktop-esr/"]
            # If product url links outside of /firefox/all/ ignore it. (e.g. testflight)
            product_urls = [url for url in product_urls if url.startswith("/en-US/firefox/all/")]
            for url in product_urls:
                doc = get_web_page(f"{base_url}{url}")
                platform_urls = [a.attrib["href"] for a in doc("ul.c-platform-list a")]
                for url in platform_urls:
                    doc = get_web_page(f"{base_url}{url}")
                    lang_urls = [a.attrib["href"] for a in doc("ul.c-lang-list a")]
                    for url in lang_urls:
                        doc = get_web_page(f"{base_url}{url}")
                        download_urls = [a.attrib["href"] for a in doc("a.download-link")]
                        for url in download_urls:
                            urls.append(url)
            assert urls
            metafunc.parametrize("download_path_l10n", urls)


def get_web_page(url):
    try:
        r = requests.get(url, timeout=TIMEOUT, headers={"accept-language": "en"})
    except requests.RequestException:
        # retry
        r = requests.get(url, timeout=TIMEOUT, headers={"accept-language": "en"})
    return pq(r.content)
