# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest
from selenium.webdriver.common.by import By

from pages.pocket.about import AboutPage

pytestmark = pytest.mark.pocket_mode


@pytest.mark.nondestructive
def test_mobile_menu(pocket_base_url, selenium_mobile):
    page = AboutPage(selenium_mobile, pocket_base_url).open()
    assert page.navigation.is_mobile_menu_open_button_displayed
    page.navigation.open_mobile_menu()
    assert page.navigation.is_mobile_menu_nav_list_displayed

    assert page.navigation.is_mobile_menu_close_button_displayed
    page.navigation.close_mobile_menu()
    assert not page.navigation.is_mobile_menu_nav_list_displayed


@pytest.mark.nondestructive
def test_accessible_mobile_menu_open_name(pocket_base_url, selenium_mobile):
    page = AboutPage(selenium_mobile, pocket_base_url).open()
    button_label_reference = page.navigation.mobile_menu_open_button.get_attribute("aria-labelledby")
    string = page.navigation.mobile_menu_open_button.find_element(By.ID, button_label_reference).text
    assert len(string) > 0


@pytest.mark.nondestructive
def test_accessible_mobile_menu_close_name(pocket_base_url, selenium_mobile):
    page = AboutPage(selenium_mobile, pocket_base_url).open()
    page.navigation.open_mobile_menu()
    string = page.navigation.mobile_menu_close_button.text
    assert len(string) > 0


@pytest.mark.nondestructive
def test_mobile_menu_not_displayed_on_desktop(pocket_base_url, selenium):
    page = AboutPage(selenium, pocket_base_url).open()
    assert not page.navigation.is_mobile_menu_open_button_displayed
