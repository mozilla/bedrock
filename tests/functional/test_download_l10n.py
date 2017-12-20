# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from bs4 import BeautifulSoup
import pytest
import requests


def pytest_generate_tests(metafunc):
    markexpr = metafunc.config.option.markexpr
    if markexpr and markexpr != 'download':
        return  # only run when specifically selected
    base_url = metafunc.config.option.base_url
    if not base_url:
        pytest.skip(
            'This test requires a base URL to be specified on the command '
            'line or in a configuration file.')
    paths = (
        '/firefox/all/',
        '/firefox/beta/all/',
        '/firefox/developer/all/',
        '/firefox/nightly/all/',
        '/firefox/organizations/all/',
        '/firefox/android/all/',
        '/firefox/android/beta/all/',
        '/firefox/android/nightly/all/',
    )
    argvalues = []
    for path in paths:
        try:
            r = requests.get(base_url + path)
        except requests.RequestException:
            r = requests.get(base_url + path)
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table', class_='build-table')
        urls = [a['href'] for a in table.find_all('a')]
        # Bug 1321262 skip broken feccec link for 'be' until bug is resolved
        urls = [url for url in urls if 'product=fennec-latest&os=android&lang=be' not in url]
        assert len(urls) > 0
        argvalues.extend(urls)
    metafunc.parametrize('url', argvalues)


@pytest.mark.download
@pytest.mark.nondestructive
def test_localized_download_links(url):
    r = requests.head(url, allow_redirects=True)
    assert requests.codes.ok == r.status_code
