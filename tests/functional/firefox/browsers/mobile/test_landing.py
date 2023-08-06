# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.browsers.mobile_landing import FirefoxMobilePage


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_download_links_displayed(base_url, selenium):
    page = FirefoxMobilePage(selenium, base_url).open()
    assert page.is_android_download_link_displayed
    assert page.is_ios_download_link_displayed
    page.focus_menu_list.click()
    assert page.focus_menu_list.list_is_open
