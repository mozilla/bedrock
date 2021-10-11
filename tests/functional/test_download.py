# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import requests

TIMEOUT = 60


def run_download_link_check(url):
    r = requests.head(url, allow_redirects=True, timeout=TIMEOUT)
    assert requests.codes.ok == r.status_code


@pytest.mark.download
@pytest.mark.nondestructive
def test_download_links(download_path):
    run_download_link_check(download_path)


@pytest.mark.download
@pytest.mark.nondestructive
def test_localized_download_links(download_path_l10n):
    run_download_link_check(download_path_l10n)
