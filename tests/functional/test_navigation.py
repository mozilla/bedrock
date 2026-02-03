# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.home import HomePage


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_navigation(base_url, selenium):
    page = HomePage(selenium, base_url, locale="de").open()

    page.navigation.open_products_menu()
    assert page.navigation.is_products_menu_displayed

    page.navigation.open_about_menu()
    assert page.navigation.is_about_menu_displayed
    assert not page.navigation.is_products_menu_displayed
