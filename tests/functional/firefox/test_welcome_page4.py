# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from selenium.common.exceptions import TimeoutException
from pages.firefox.welcome.page4 import FirefoxWelcomePage4


@pytest.mark.nondestructive
def test_modal_button_displayed(base_url, selenium):
    page = FirefoxWelcomePage4(selenium, base_url).open()
    assert page.is_primary_modal_button_displayed
    assert page.is_secondary_modal_button_displayed


@pytest.mark.nondestructive
def test_get_firefox_qr_code(base_url, selenium):
    page = FirefoxWelcomePage4(selenium, base_url, locale='sv-SE').open()
    modal = page.click_primary_modal_button()
    assert modal.is_displayed
    assert not page.send_to_device.is_displayed
    assert page.is_firefox_qr_code_displayed
    modal.close()


@pytest.mark.nondestructive
def test_primary_get_firefox_send_to_device_success(base_url, selenium):
    page = FirefoxWelcomePage4(selenium, base_url).open()
    modal = page.click_primary_modal_button()
    assert modal.is_displayed
    assert not page.is_firefox_qr_code_displayed
    send_to_device = page.send_to_device
    send_to_device.type_email('success@example.com')
    send_to_device.click_send()
    assert send_to_device.send_successful
    modal.close()


@pytest.mark.nondestructive
def test_get_firefox_send_to_device_fails_when_missing_required_fields(base_url, selenium):
    page = FirefoxWelcomePage4(selenium, base_url).open()
    modal = page.click_primary_modal_button()
    assert modal.is_displayed
    with pytest.raises(TimeoutException):
        page.send_to_device.click_send()
