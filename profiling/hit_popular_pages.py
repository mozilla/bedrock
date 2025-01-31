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
    "/en-US/firefox/",
    "/en-US/firefox/121.0/system-requirements/",
    "/en-US/firefox/download/all/",
    "/en-US/firefox/android/124.0/releasenotes/",
    "/en-US/firefox/channel/desktop/",
    "/en-US/firefox/channel/desktop/?reason=manual-update",
    "/en-US/firefox/developer/",
    "/en-US/firefox/download/",
    "/en-US/firefox/download/thanks/",
    "/en-US/firefox/download/thanks/?s=direct",
    "/en-US/firefox/enterprise/",
    "/en-US/firefox/features/",
    "/en-US/firefox/installer-help/?channel=release&installer_lang=en-US",
    "/en-US/firefox/releases/",
    "/en-US/firefox/set-as-default/thanks/",
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
