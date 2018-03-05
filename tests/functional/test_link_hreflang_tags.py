# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import requests


LINK_TEMPLATE = '<link rel="canonical" href="{url}">'


@pytest.mark.headless
@pytest.mark.nondestructive
@pytest.mark.parametrize('url,locales', [
    ('/firefox/new/', ('en-US', 'de', 'id')),
    ('/firefox/', ('en-US', 'de', 'id')),
    ('/', ('en-US', 'de', 'id')),
])
def test_link_hreflang_tags(url, locales, base_url):
    for locale in locales:
        full_url = '{}/{}{}'.format(base_url, locale, url)
        link_url = '{}/{}{}'.format('https://www.mozilla.org', locale, url)
        resp = requests.get(full_url, timeout=5)
        assert LINK_TEMPLATE.format(url=link_url) in resp.content
