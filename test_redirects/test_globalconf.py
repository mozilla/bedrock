"""Test redirects from the global.conf file."""
from __future__ import absolute_import

from .base import assert_valid_url


# uses pytest fixtures found in conftest.py

def test_global_conf_url(global_conf_url):
    # tests defined in map_globalconf.py
    assert_valid_url(**global_conf_url)
