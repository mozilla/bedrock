# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.partners import PartnersPage


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_partner_menu(base_url, selenium):
    page = PartnersPage(base_url, selenium).open()
    assert page.is_phone_overview_screen_displayed
    assert not page.is_phone_os_screen_displayed
    assert not page.is_phone_marketplace_screen_displayed
    assert not page.is_android_phone_displayed

    page.partner_menu.show_firefox_os()
    assert page.is_phone_os_screen_displayed

    page.partner_menu.show_marketplace()
    assert page.is_phone_marketplace_screen_displayed

    page.partner_menu.show_android()
    assert page.is_android_phone_displayed

    page.partner_menu.show_overview()
    assert page.is_phone_overview_screen_displayed


@pytest.mark.nondestructive
def test_mwc_navigation(base_url, selenium):
    page = PartnersPage(base_url, selenium).open()
    modal = page.mwc_menu.show_map()
    assert modal.is_displayed
    modal.close()
    modal = page.mwc_menu.show_schedule()
    assert modal.is_displayed
    modal.close()


@pytest.mark.nondestructive
def test_devices_menu(base_url, selenium):
    page = PartnersPage(base_url, selenium).open()
    devices_page = page.devices_menu.show_devices()
    assert devices_page.url in selenium.current_url


@pytest.mark.nondestructive
def test_firefox_os_menu(base_url, selenium):
    page = PartnersPage(base_url, selenium).open()
    page.partner_menu.show_firefox_os()
    for item in reversed(page.firefox_os.menu.items):
        item.click()
        assert page.firefox_os.section == item.id


@pytest.mark.nondestructive
def test_marketplace_menu(base_url, selenium):
    page = PartnersPage(base_url, selenium).open()
    page.partner_menu.show_marketplace()
    for item in reversed(page.marketplace.menu.items):
        item.click()
        assert page.marketplace.section == item.id


@pytest.mark.nondestructive
def test_android_menu(base_url, selenium):
    page = PartnersPage(base_url, selenium).open()
    page.partner_menu.show_android()
    for item in reversed(page.android.menu.items):
        item.click()
        assert page.android.section == item.id
