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
    "/en-US/firefox/126.0/whatsnew/",
    "/en-US/firefox/",
    "/en-US/firefox/windows/",
    "/en-US/firefox/download/thanks/",
    "/en-US/firefox/features/",
    "/en-US/firefox/all/",
    "/en-US/",
    "/en-US/firefox/installer-help/?channel=release&installer_lang=en-US",
    "/en-US/firefox/download/thanks/?s=direct",
    "/en-US/firefox/welcome/19/",
    "/en-US/firefox/enterprise/?reason=manual-update",
    "/en-US/products/vpn/",
    "/en-US/firefox/browsers/windows-64-bit/",
    "/en-US/firefox/mac/",
    "/en-US/about/",
    "/en-US/firefox/android/124.0/releasenotes/",
    "/en-US/firefox/browsers/mobile/get-app/",
    "/en-US/firefox/browsers/",
    "/en-US/firefox/nightly/firstrun/",
    "/en-US/firefox/developer/",
    "/en-US/account/",
    "/en-US/contribute/",
    "/en-US/firefox/browsers/mobile/android/",
    "/en-US/privacy/archive/firefox-fire-tv/2023-06/",
    "/en-US/firefox/121.0/system-requirements/",
    "/en-US/firefox/browsers/mobile/",
    "/en-US/firefox/releases/",
    "/en-US/MPL/",
    "/en-US/firefox/enterprise/",
    "/en-US/security/advisories/",
    "/en-US/firefox/browsers/what-is-a-browser/",
    "/en-US/firefox/channel/desktop/?reason=manual-update",
    "/en-US/firefox/pocket/",
    "/en-US/firefox/channel/desktop/",
    "/en-US/firefox/welcome/17b/",
    "/en-US/firefox/welcome/17c/",
    "/en-US/firefox/welcome/17a/",
    "/en-US/firefox/set-as-default/thanks/",
    "/en-US/careers/listings/",
    "/en-US/firefox/browsers/chromebook/",
    "/en-US/firefox/nothing-personal/",
    "/en-US/newsletter/existing/",
    "/en-US/about/legal/terms/firefox/",
    "/en-US/firefox/linux/",
    "/en-US/firefox/browsers/mobile/focus/",
    "/en-US/products/vpn/download/",
    "/en-US/about/manifesto/",
    "/en-US/stories/joy-of-color/",
    "/en-US/contact/",
    "/en-US/about/legal/defend-mozilla-trademarks/",
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
