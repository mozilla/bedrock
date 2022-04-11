# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.home import FirefoxHomePage


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_download_menu_list_displays(base_url, selenium):
    page = FirefoxHomePage(selenium, base_url).open()
    page.browser_menu_list.click()
    assert page.browser_menu_list.list_is_open


@pytest.mark.nondestructive
def test_sticky_promo(base_url, selenium):
    page = FirefoxHomePage(selenium, base_url).open()
    page.init_promo()
    assert page.promo.is_displayed
    page.promo.close()
    assert not page.promo.is_displayed
