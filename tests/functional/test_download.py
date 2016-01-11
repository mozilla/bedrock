# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from bs4 import BeautifulSoup
import pytest
import requests


def pytest_generate_tests(metafunc):
    paths = (
        '/firefox/new/',
        '/thunderbird/')
    argvalues = []
    for path in paths:
        r = requests.get(metafunc.config.option.base_url + path)
        soup = BeautifulSoup(r.content, 'html.parser')
        urls = [a['href'] for a in soup.find('ul', class_='download-list').find_all('a')]
        assert len(urls) > 0
        argvalues.extend(urls)
    metafunc.parametrize('url', argvalues)


@pytest.mark.headless
def test_download_links(url):
    r = requests.head(url, allow_redirects=True)
    assert requests.codes.ok == r.status_code
