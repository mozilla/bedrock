# -*- coding: utf-8 -*-

from __future__ import absolute_import

import requests

from .base import flatten, url_test

URLS = flatten((
    url_test('https://www.mozilla.com/', 'https://www.mozilla.org/firefox/'),
    url_test('https://aurora.mozilla.org/', 'https://www.mozilla.org/firefox/aurora/', status_code=requests.codes.found),
    url_test('https://beta.mozilla.org/', 'https://www.mozilla.org/en-US/firefox/channel/#beta'),
))
