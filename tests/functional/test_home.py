# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.home import HomePage


@pytest.mark.skipif(reason='https://bugzilla.mozilla.org/show_bug.cgi?id=1392501')  # Q3 homepage test
@pytest.mark.sanity
@pytest.mark.nondestructive
def test_download_button_is_displayed(base_url, selenium):
    page = HomePage(selenium, base_url).open()
    assert page.download_button.is_displayed


@pytest.mark.skipif(reason='https://bugzilla.mozilla.org/show_bug.cgi?id=1392501')  # Q3 homepage test
@pytest.mark.sanity
@pytest.mark.smoke
@pytest.mark.nondestructive
def test_get_firefox_link_is_displayed(base_url, selenium):
    page = HomePage(selenium, base_url).open()
    assert page.is_get_firefox_link_displayed
