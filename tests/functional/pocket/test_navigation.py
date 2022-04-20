# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest
from selenium.webdriver.common.by import By

from pages.pocket.about import AboutPage


@pytest.mark.skip(reason="Disabled until we have a Pocket-mode server to test against - see #11509")
@pytest.mark.nondestructive
def test_mobile_menu(base_url, selenium_mobile):
    page = AboutPage(selenium_mobile, base_url).open()
    assert page.navigation.is_mobile_menu_open_button_displayed
    page.navigation.open_mobile_menu()
    assert page.navigation.is_mobile_menu_home_link_displayed
    assert page.navigation.is_mobile_menu_my_list_link_displayed

    assert page.navigation.is_mobile_menu_close_button_displayed
    page.navigation.close_mobile_menu()
    assert not page.navigation.is_mobile_menu_home_link_displayed
    assert not page.navigation.is_mobile_menu_my_list_link_displayed


@pytest.mark.skip(reason="Disabled until we have a Pocket-mode server to test against - see #11509")
def test_accessible_mobile_menu_open_name(base_url, selenium_mobile):
    page = AboutPage(selenium_mobile, base_url).open()
    button_label_reference = page.navigation.mobile_menu_open_button.get_attribute("aria-labelledby")
    string = page.navigation.mobile_menu_open_button.find_element(By.ID, button_label_reference).text
    assert len(string) > 0


@pytest.mark.skip(reason="Disabled until we have a Pocket-mode server to test against - see #11509")
def test_accessible_mobile_menu_close_name(base_url, selenium_mobile):
    page = AboutPage(selenium_mobile, base_url).open()
    page.navigation.open_mobile_menu()
    string = page.navigation.mobile_menu_close_button.text
    assert len(string) > 0
