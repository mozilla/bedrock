# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from selenium.common.exceptions import TimeoutException
from pages.firefox.mobile import FirefoxMobilePage


@pytest.mark.nondestructive
def test_get_firefox_send_to_device_success(base_url, selenium):
    page = FirefoxMobilePage(selenium, base_url).open()
    modal = page.click_get_firefox_header_button()
    assert modal.is_displayed
    assert not page.is_firefox_qr_code_displayed
    send_to_device = page.send_to_device
    send_to_device.type_email('success@example.com')
    send_to_device.click_send()
    assert send_to_device.send_successful
    modal.close()


@pytest.mark.nondestructive
def test_get_firefox_send_to_device_fails_when_missing_required_fields(base_url, selenium):
    page = FirefoxMobilePage(selenium, base_url).open()
    modal = page.click_get_firefox_header_button()
    assert modal.is_displayed
    with pytest.raises(TimeoutException):
        page.send_to_device.click_send()


@pytest.mark.nondestructive
def test_get_firefox_qr_code_locale(base_url, selenium):
    page = FirefoxMobilePage(selenium, base_url, locale='it').open()
    modal = page.click_get_firefox_header_button()
    assert modal.is_displayed
    assert not page.send_to_device.is_displayed
    assert page.is_firefox_qr_code_displayed
    modal.close()


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_get_focus_header_button(base_url, selenium):
    page = FirefoxMobilePage(selenium, base_url).open()
    modal = page.click_get_focus_header_button()
    assert modal.is_displayed
    assert page.is_focus_qr_code_displayed
    modal.close()


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_get_firefox_nav_button(base_url, selenium):
    page = FirefoxMobilePage(selenium, base_url).open()
    modal = page.click_get_firefox_nav_button()
    assert modal.is_displayed
    assert page.send_to_device.is_displayed
    assert not page.is_firefox_qr_code_displayed
    modal.close()


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_get_focus_nav_button(base_url, selenium):
    page = FirefoxMobilePage(selenium, base_url).open()
    modal = page.click_get_focus_nav_button()
    assert modal.is_displayed
    assert page.is_focus_qr_code_displayed
    modal.close()
