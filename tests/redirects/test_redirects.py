"""Test redirects from the global.conf file."""
from __future__ import absolute_import
from operator import itemgetter

import pytest

from .base import assert_valid_url
from .map_301 import URLS as REDIRECT_URLS
from .map_htaccess import URLS as HTA_URLS
from .map_globalconf import URLS as GLOBAL_URLS
from .map_locales import URLS as LOCALE_URLS


@pytest.mark.smoke
@pytest.mark.headless
@pytest.mark.nondestructive
@pytest.mark.django_db
@pytest.mark.parametrize('url', REDIRECT_URLS, ids=itemgetter('url'))
def test_301_url(url, base_url):
    url['base_url'] = base_url
    assert_valid_url(**url)


@pytest.mark.smoke
@pytest.mark.headless
@pytest.mark.nondestructive
@pytest.mark.django_db
@pytest.mark.parametrize('url', GLOBAL_URLS, ids=itemgetter('url'))
def test_global_conf_url(url, base_url):
    url['base_url'] = base_url
    assert_valid_url(**url)


@pytest.mark.smoke
@pytest.mark.headless
@pytest.mark.nondestructive
@pytest.mark.django_db
@pytest.mark.parametrize('url', HTA_URLS, ids=itemgetter('url'))
def test_htaccess_url(url, base_url):
    url['base_url'] = base_url
    assert_valid_url(**url)


@pytest.mark.smoke
@pytest.mark.headless
@pytest.mark.nondestructive
@pytest.mark.django_db
@pytest.mark.parametrize('url', LOCALE_URLS)
def test_locale_url(url, base_url):
    url['base_url'] = base_url
    assert_valid_url(**url)
