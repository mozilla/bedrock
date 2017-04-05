# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from selenium.common.exceptions import TimeoutException

from pages.firefox.ios import IOSPage


@pytest.mark.nondestructive
def test_send_to_device_sucessful_submission(base_url, selenium):
    page = IOSPage(selenium, base_url, locale='de').open()
    send_to_device = page.send_to_device
    send_to_device.type_email('success@example.com')
    send_to_device.click_send()
    assert send_to_device.send_successful


@pytest.mark.nondestructive
def test_send_to_device_fails_when_missing_required_fields(base_url, selenium):
    page = IOSPage(selenium, base_url, locale='de').open()
    with pytest.raises(TimeoutException):
        page.send_to_device.click_send()


@pytest.mark.nondestructive
def test_send_to_device_not_supported_locale(base_url, selenium):
    page = IOSPage(selenium, base_url, locale='it').open()
    assert page.is_app_store_button_displayed
    assert not page.send_to_device.is_displayed
