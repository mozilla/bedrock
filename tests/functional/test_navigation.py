# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.home import HomePage


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_navigation(base_url, selenium):
    page = HomePage(selenium, base_url, locale="de").open()
    page.navigation.open_firefox_menu()
    assert page.navigation.is_firefox_menu_displayed

    page.navigation.open_products_menu()
    assert page.navigation.is_products_menu_displayed
    assert not page.navigation.is_firefox_menu_displayed

    page.navigation.open_about_menu()
    assert page.navigation.is_about_menu_displayed
    assert not page.navigation.is_products_menu_displayed

    page.navigation.open_innovation_menu()
    assert page.navigation.is_innovation_menu_displayed
    assert not page.navigation.is_about_menu_displayed


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_mobile_navigation(base_url, selenium_mobile):
    page = HomePage(selenium_mobile, base_url, locale="de").open()
    page.navigation.show()
    page.navigation.open_firefox_menu()
    assert page.navigation.is_firefox_menu_displayed

    page.navigation.open_products_menu()
    assert page.navigation.is_products_menu_displayed

    page.navigation.open_about_menu()
    assert page.navigation.is_about_menu_displayed

    page.navigation.open_innovation_menu()
    assert page.navigation.is_innovation_menu_displayed


@pytest.mark.smoke
@pytest.mark.nondestructive
@pytest.mark.skip_if_firefox(reason="Firefox download button is shown only to non-Firefox users.")
def test_navigation_download_firefox_button(base_url, selenium):
    page = HomePage(selenium, base_url, locale="de").open()
    assert not page.navigation.is_mozilla_vpn_button_displayed
    assert page.navigation.is_firefox_download_button_displayed


@pytest.mark.nondestructive
@pytest.mark.skip_if_not_firefox(reason="Mozilla VPN button is shown only to Firefox users.")
def test_navigation_mozilla_vpn_button(base_url, selenium):
    page = HomePage(selenium, base_url, locale="de").open()
    assert not page.navigation.is_firefox_download_button_displayed
    assert page.navigation.is_mozilla_vpn_button_displayed
