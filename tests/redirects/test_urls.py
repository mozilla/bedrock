# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""Test redirects from the global.conf file."""

import pytest
import requests

from bedrock import settings

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
    assert_valid_url(
        "/en-US/abck",
        base_url=base_url,
        final_status_code=requests.codes.not_found,
        follow_redirects=True,
    )


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
        "/firefox/nightly/whatsnew/",
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


@pytest.mark.skipif(
    settings.ENABLE_FIREFOX_COM_REDIRECTS is True,
    reason="Redirected offsite now. [TODO] Make a new list of key locale fixups.",
)
@pytest.mark.headless
@pytest.mark.nondestructive
@pytest.mark.django_db
@pytest.mark.parametrize(
    "url",
    [
        "/firefox/all/",
        "/firefox/developer/",
        "/firefox/installer-help/",
        "/firefox/new/",
        "/firefox/unsupported-systems/",
    ],
)
def test_302_fx_urls(url, base_url, follow_redirects=False):
    assert_valid_url(url, base_url=base_url, follow_redirects=follow_redirects, status_code=requests.codes.found)


@pytest.mark.headless
@pytest.mark.nondestructive
@pytest.mark.django_db
@pytest.mark.parametrize(
    "url",
    [
        "/firefox/latest/releasenotes/",
        "/firefox/releasenotes/",
        "/firefox/notes/",
        "/firefox/system-requirements/",
        "/firefox/nightly/firstrun/",
        "/firefox/releases/",
        "/firefox/android/releasenotes/",
        "/firefox/ios/releasenotes/",
    ],
)
def test_302_fx_urls_kept(url, base_url, follow_redirects=False):
    assert_valid_url(url, base_url=base_url, follow_redirects=follow_redirects, status_code=requests.codes.found)
