# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from bs4 import BeautifulSoup
import pytest
import requests


PAGE_PATHS = (
    '/firefox/all/',
    '/firefox/beta/all/',
    '/firefox/developer/all/',
    '/firefox/nightly/all/',
    '/firefox/organizations/all/',
    '/firefox/android/all/',
    '/firefox/android/beta/all/',
    '/firefox/android/nightly/all/',
)


@pytest.mark.download
@pytest.mark.nondestructive
@pytest.mark.parametrize('path', PAGE_PATHS)
def test_localized_download_links(path, base_url):
    if not base_url:
        pytest.skip(
            'This test requires a base URL to be specified on the command '
            'line or in a configuration file.')

    full_url = base_url + '/en-US' + path
    try:
        r = requests.get(full_url)
    except requests.RequestException:
        # retry
        r = requests.get(full_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('table', class_='build-table')
    urls = [a['href'] for a in table.find_all('a')]
    assert urls
    for url in urls:
        r = requests.head(url, allow_redirects=True)
        assert requests.codes.ok == r.status_code
