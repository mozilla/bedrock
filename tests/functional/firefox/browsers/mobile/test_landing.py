# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.browsers.mobile_landing import FirefoxMobilePage


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_download_links_displayed(base_url, selenium):
    page = FirefoxMobilePage(selenium, base_url, params="?xv=current").open()
    assert page.is_android_download_link_displayed
    assert page.is_ios_download_link_displayed
    page.focus_menu_list.click()
    assert page.focus_menu_list.list_is_open


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_send_to_device_success(base_url, selenium):
    page = FirefoxMobilePage(selenium, base_url, params="?xv=legacy").open()
    send_to_device = page.send_to_device
    send_to_device.type_email("success@example.com")
    send_to_device.click_send()
    assert send_to_device.send_successful


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_send_to_device_failure(base_url, selenium):
    page = FirefoxMobilePage(selenium, base_url, params="?xv=legacy").open()
    send_to_device = page.send_to_device
    send_to_device.type_email("failure@example.com")
    send_to_device.click_send(expected_result="error")
    assert send_to_device.is_form_error_displayed
