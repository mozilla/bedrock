# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.home import FirefoxHomePage


@pytest.mark.sanity
@pytest.mark.nondestructive
def test_download_menu_list_displayes(base_url, selenium):
    page = FirefoxHomePage(selenium, base_url).open()
    page.browser_menu_list.click()
    assert page.browser_menu_list.list_is_open


@pytest.mark.nondestructive
@pytest.mark.skip_if_not_firefox(reason='FB Container link shown only to Firefox users.')
def test_fb_container_fx(base_url, selenium):
    page = FirefoxHomePage(selenium, base_url).open()
    assert page.fb_container_is_displayed


@pytest.mark.nondestructive
@pytest.mark.skip_if_firefox(reason='FB Container link hidden from non Firefox users.')
def test_fb_container_non_fx(base_url, selenium):
    page = FirefoxHomePage(selenium, base_url).open()
    assert not page.fb_container_is_displayed
