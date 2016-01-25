# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from selenium.common.exceptions import TimeoutException

from pages.firefox.ios import IOSPage


@pytest.mark.flaky(reruns=1, reason='https://bugzilla.mozilla.org/show_bug.cgi?id=1218451')
def test_send_to_device_sucessful_submission(base_url, selenium):
    page = IOSPage(base_url, selenium).open()
    page.click_get_it_now()
    send_to_device = page.send_to_device
    assert page.send_to_device.is_displayed
    send_to_device.type_email('noreply@mozilla.com')
    send_to_device.click_send()
    assert send_to_device.send_successful


@pytest.mark.nondestructive
def test_send_to_device_fails_when_missing_required_fields(base_url, selenium):
    page = IOSPage(base_url, selenium).open()
    with pytest.raises(TimeoutException):
        page.click_get_it_now()
        page.send_to_device.click_send()


@pytest.mark.nondestructive
def test_send_to_device_not_supported_locale(base_url, selenium):
    page = IOSPage(base_url, selenium, locale='it').open()
    assert page.is_app_store_button_displayed
    assert not page.is_get_it_now_button_displayed
