"""Test redirects from the global.conf file."""
from __future__ import absolute_import
from operator import itemgetter

import pytest

from .base import assert_valid_url
from .map_globalconf import URLS as GLOBAL_URLS


@pytest.mark.parametrize('url', GLOBAL_URLS, ids=itemgetter('url'))
def test_global_conf_url(url, live_or_remote_server):
    # live_or_remote_server defined in conftest.py
    url['base_url'] = live_or_remote_server
    assert_valid_url(**url)
