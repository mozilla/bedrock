# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""Request a selection of pages that are populat on www.m.o from your local
runserver, so  that django-silk can capture performance info on them.

Usage:

    1. In your .env set ENABLE_DJANGO_SILK=True
    2. Start your runserver on port 8000
    3. python profiling/hit_popular_pages.py
    3. View results at http://localhost:8000/silk/

"""

import sys
import time

import requests

paths = [
    "/en-US/firefox/140.0/whatsnew/",
    "/zh-TW/firefox/120.0/whatsnew/",
    "/en-US/firefox/download/thanks/",
    "/en-US/firefox/download/thanks/?s=direct",
    "/en-US/",
    "/de/",
    "/en-US/about/",
    "/pt-BR/about/",
    "/sv-SE/firefox/browsers/mobile/get-app/",
    "/en-US/firefox/browsers/mobile/get-app/",
    "/en-US/firefox/nightly/firstrun/",
    "/en-US/products/vpn/",
    "/en-US/products/vpn/download/",
    "/en-US/account/",
    "/en-US/contribute/",
    "/en-US/privacy/archive/firefox-fire-tv/2023-06/",
    "/en-US/MPL/",
    "/en-US/security/advisories/",
    "/en-US/firefox/welcome/19/",
    "/en-US/firefox/welcome/17c/",
    "/en-US/firefox/welcome/17b/",
    "/en-US/firefox/welcome/17a/",
    "/en-US/firefox/nothing-personal/",
    "/en-US/newsletter/existing/",
    "/en-US/about/legal/terms/firefox/",
    "/en-US/about/legal/defend-mozilla-trademarks/",
    "/en-US/about/manifesto/",
    "/en-US/careers/listings/",
    "/en-US/contact/",
]


def _log(*args):
    sys.stdout.write("\n".join(args))


def hit_pages(paths, times=3):
    _base_url = "http://localhost:8000"

    for path in paths:
        for _ in range(times):
            time.sleep(0.5)
            url = f"{_base_url}{path}"
            requests.get(url)

    _log("All done")


if __name__ == "__main__":
    hit_pages(paths)
