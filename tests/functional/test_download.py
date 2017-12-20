# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from bs4 import BeautifulSoup
import pytest
import requests


def pytest_generate_tests(metafunc):
    markexpr = metafunc.config.option.markexpr
    if markexpr and markexpr != 'download':
        return  # test deslected by mark expression
    base_url = metafunc.config.option.base_url
    if not base_url:
        pytest.skip(
            'This test requires a base URL to be specified on the command '
            'line or in a configuration file.')
    paths = (
        '/firefox/new/?scene=2',
        '/thunderbird/')
    argvalues = []
    for path in paths:
        try:
            r = requests.get(base_url + path)
        except requests.RequestException:
            r = requests.get(base_url + path)
        soup = BeautifulSoup(r.content, 'html.parser')
        urls = [a['href'] for a in soup.find('ul', class_='download-list').find_all('a')]
        # Bug 1266682 remove links to Play Store to avoid rate limiting in automation.
        for url in urls:
            if 'play.google.com' in url:
                urls.remove(url)
        assert len(urls) > 0
        argvalues.extend(urls)
    metafunc.parametrize('url', argvalues)


@pytest.mark.download
@pytest.mark.nondestructive
def test_download_links(url):
    r = requests.head(url, allow_redirects=True)
    assert requests.codes.ok == r.status_code
