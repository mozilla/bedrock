"""Test redirects from the global.conf file."""
from __future__ import absolute_import
from operator import itemgetter

import pytest
import requests

from .base import assert_valid_url
from .map_410 import URLS_410
from .map_htaccess import URLS as HTA_URLS
from .map_globalconf import URLS as GLOBAL_URLS
from .map_external import URLS as EXTERNAL_URLS
from .map_locales import URLS as LOCALE_URLS


@pytest.mark.smoke
@pytest.mark.headless
@pytest.mark.nondestructive
@pytest.mark.parametrize('url', GLOBAL_URLS, ids=itemgetter('url'))
def test_global_conf_url(url, base_url):
    url['base_url'] = base_url
    assert_valid_url(**url)


@pytest.mark.smoke
@pytest.mark.headless
@pytest.mark.nondestructive
@pytest.mark.parametrize('url', HTA_URLS, ids=itemgetter('url'))
def test_htaccess_url(url, base_url):
    url['base_url'] = base_url
    assert_valid_url(**url)


@pytest.mark.smoke
@pytest.mark.headless
@pytest.mark.nondestructive
@pytest.mark.parametrize('url', LOCALE_URLS)
def test_locale_url(url, base_url):
    url['base_url'] = base_url
    assert_valid_url(**url)


@pytest.mark.headless
@pytest.mark.nondestructive
@pytest.mark.parametrize('url', EXTERNAL_URLS, ids=itemgetter('url'))
def test_external_url(url):
    assert_valid_url(**url)


@pytest.mark.smoke
@pytest.mark.headless
@pytest.mark.nondestructive
@pytest.mark.parametrize('url', URLS_410)
def test_410_url(url, base_url):
    assert_valid_url(url, status_code=requests.codes.gone, base_url=base_url)


@pytest.mark.smoke
@pytest.mark.headless
@pytest.mark.nondestructive
def test_404_url(base_url):
    assert_valid_url(
        '/en-US/abck',
        status_code=requests.codes.not_found,
        base_url=base_url)


@pytest.mark.smoke
@pytest.mark.headless
@pytest.mark.nondestructive
def test_x_robots_tag(base_url):
    assert_valid_url(base_url, resp_headers={'x-robots-tag': 'noodp'})
