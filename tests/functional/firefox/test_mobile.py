# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from selenium.common.exceptions import TimeoutException
from pages.firefox.mobile import FirefoxMobilePage


# mobile - send to device


# Protocol
@pytest.mark.nondestructive
def test_get_firefox_send_to_device_success(base_url, selenium):
    page = FirefoxMobilePage(selenium, base_url).open()
    modal = page.click_get_firefox_button()
    assert modal.is_displayed
    assert not page.is_firefox_qr_code_displayed
    send_to_device = page.send_to_device
    send_to_device.type_email('success@example.com')
    send_to_device.click_send()
    assert send_to_device.send_successful


# Protocol
@pytest.mark.nondestructive
def test_get_firefox_send_to_device_fails_when_missing_required_fields(base_url, selenium):
    page = FirefoxMobilePage(selenium, base_url).open()
    modal = page.click_get_firefox_button()
    assert modal.is_displayed
    with pytest.raises(TimeoutException):
        page.send_to_device.click_send()


# Pebbles
@pytest.mark.nondestructive
def test_get_firefox_send_to_device_success_locale(base_url, selenium):
    page = FirefoxMobilePage(selenium, base_url, locale='fr').open()
    modal = page.click_get_firefox_button()
    assert modal.is_displayed
    assert not page.is_firefox_qr_code_displayed
    send_to_device = page.send_to_device
    send_to_device.type_email('success@example.com')
    send_to_device.click_send()
    assert send_to_device.send_successful
    modal.close()


# Pebbles
@pytest.mark.nondestructive
def test_get_firefox_send_to_device_fails_when_missing_required_fields_locale(base_url, selenium):
    page = FirefoxMobilePage(selenium, base_url, locale='fr').open()
    modal = page.click_get_firefox_button()
    assert modal.is_displayed
    with pytest.raises(TimeoutException):
        page.send_to_device.click_send()


# mobile - qr code


# Protocol
@pytest.mark.nondestructive
def test_get_firefox_qr_code(base_url, selenium):
    page = FirefoxMobilePage(selenium, base_url, locale='en-CA').open()
    modal = page.click_get_firefox_button()
    assert modal.is_displayed
    assert not page.send_to_device.is_displayed
    assert page.is_firefox_qr_code_displayed


# Pebbles
@pytest.mark.nondestructive
def test_get_firefox_qr_code_locale(base_url, selenium):
    page = FirefoxMobilePage(selenium, base_url, locale='it').open()
    modal = page.click_get_firefox_button()
    assert modal.is_displayed
    assert not page.send_to_device.is_displayed
    assert page.is_firefox_qr_code_displayed
    modal.close()


# focus - qr code


# Protocol
@pytest.mark.nondestructive
def test_get_focus_header_button(base_url, selenium):
    page = FirefoxMobilePage(selenium, base_url).open()
    modal = page.click_get_focus_button()
    assert modal.is_displayed
    assert page.is_focus_qr_code_displayed


# Pebbles
@pytest.mark.nondestructive
def test_get_focus_header_button_locale(base_url, selenium):
    page = FirefoxMobilePage(selenium, base_url, locale='fr').open()
    modal = page.click_get_focus_button()
    assert modal.is_displayed
    assert page.is_focus_qr_code_displayed
    modal.close()


# scroll to section - Pebbles only


# Pebbles
@pytest.mark.nondestructive
def test_get_firefox_features_button_locale(base_url, selenium):
    page = FirefoxMobilePage(selenium, base_url, locale='fr').open()
    modal = page.click_get_firefox_features_button()
    assert modal.is_displayed
    assert page.send_to_device.is_displayed
    assert not page.is_firefox_qr_code_displayed
    modal.close()


# Pebbles
@pytest.mark.nondestructive
def test_get_focus_features_button_locale(base_url, selenium):
    page = FirefoxMobilePage(selenium, base_url, locale='fr').open()
    modal = page.click_get_focus_features_button()
    assert modal.is_displayed
    assert page.is_focus_qr_code_displayed
    modal.close()
