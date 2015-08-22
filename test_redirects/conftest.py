from __future__ import absolute_import

from operator import itemgetter

import pytest

from .map_globalconf import URLS as GLOBAL_URLS


@pytest.fixture(params=GLOBAL_URLS, ids=itemgetter('url'))
def global_conf_url(request):
    return request.param
