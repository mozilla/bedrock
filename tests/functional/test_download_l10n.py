# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from bs4 import BeautifulSoup
import pytest
import requests


def pytest_generate_tests(metafunc):
    if 'not headless' in metafunc.config.option.markexpr:
        return  # test deslected by mark expression
    base_url = metafunc.config.option.base_url
    if not base_url:
        pytest.skip(
            'This test requires a base URL to be specified on the command '
            'line or in a configuration file.')
    paths = (
        '/firefox/all/',
        '/firefox/beta/all/',
        '/firefox/developer/all/',
        '/firefox/organizations/all/',
        '/firefox/android/all/',
        '/firefox/android/beta/all/')
    argvalues = []
    for path in paths:
        r = requests.get(base_url + path)
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table', class_='build-table')
        urls = [a['href'] for a in table.find_all('a')]
        assert len(urls) > 0
        argvalues.extend(urls)
    metafunc.parametrize('url', argvalues)


@pytest.mark.headless
@pytest.mark.nondestructive
def test_localized_download_links(url):
    r = requests.head(url, allow_redirects=True)
    assert requests.codes.ok == r.status_code
