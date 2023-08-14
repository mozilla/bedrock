# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.home import HomePage


@pytest.mark.smoke
@pytest.mark.nondestructive
@pytest.mark.parametrize("locale", ["en-US"])
def test_product_buttons_are_dis(locale, base_url, selenium):
    page = HomePage(selenium, base_url, locale=locale).open()
    assert page.is_firefox_download_button_displayed
    assert page.is_pocket_download_button_displayed
    assert page.is_relay_download_button_displayed
    assert page.is_mozilla_vpn_download_button_displayed
