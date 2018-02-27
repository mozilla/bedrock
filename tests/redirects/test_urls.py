"""Test redirects from the global.conf file."""
from __future__ import absolute_import

import pytest
import requests

from .base import assert_valid_url
from .map_410 import URLS_410


@pytest.mark.smoke
@pytest.mark.headless
@pytest.mark.nondestructive
@pytest.mark.django_db
@pytest.mark.parametrize('url', URLS_410)
def test_410_url(url, base_url):
    assert_valid_url(url, base_url=base_url, status_code=requests.codes.gone)


@pytest.mark.smoke
@pytest.mark.headless
@pytest.mark.nondestructive
@pytest.mark.django_db
def test_404_url(base_url):
    assert_valid_url(
        '/en-US/abck',
        status_code=requests.codes.not_found,
        base_url=base_url)


@pytest.mark.smoke
@pytest.mark.headless
@pytest.mark.nondestructive
@pytest.mark.django_db
def test_x_robots_tag(base_url):
    assert_valid_url(base_url, resp_headers={'x-robots-tag': 'noodp'})


@pytest.mark.headless
@pytest.mark.nondestructive
@pytest.mark.django_db
@pytest.mark.parametrize('url', [
    '/firefox/',
    '/firefox/all/',
    '/firefox/android/',
    '/firefox/android/faq/',
    '/firefox/aurora/all/',
    '/firefox/beta/all/',
    '/firefox/brand/',
    '/firefox/channel/',
    '/firefox/desktop/',
    '/firefox/developer/',
    '/firefox/installer-help/',
    '/firefox/interest-dashboard/',
    '/firefox/latest/releasenotes/',
    '/firefox/mobile/',
    '/firefox/new/',
    '/firefox/nightly/firstrun/',
    '/firefox/organizations/',
    '/firefox/os/',
    '/firefox/os/notes/1.1/',
    '/firefox/partners/',
    '/firefox/releases/',
    '/firefox/speed/',
    '/firefox/sync/',
    '/firefox/tiles/',
    '/firefox/unsupported-systems/',
    '/firefox/unsupported/EOL/',
    # Legacy URLs (Bug 1110927)
    '/firefox/start/central.html',
    '/firefox/sync/firstrun.html'
])
def test_url(url, base_url, follow_redirects=False):
    assert_valid_url(url, base_url=base_url,
                     follow_redirects=follow_redirects)
