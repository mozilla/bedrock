# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from selenium.common.exceptions import TimeoutException

from pages.firefox.android import AndroidPage


@pytest.mark.nondestructive
def test_send_to_device_sucessful_submission(base_url, selenium):
    page = AndroidPage(selenium, base_url, locale='de').open()
    send_to_device = page.send_to_device
    send_to_device.type_email('success@example.com')
    send_to_device.click_send()
    assert send_to_device.send_successful


@pytest.mark.nondestructive
def test_send_to_device_fails_when_missing_required_fields(base_url, selenium):
    page = AndroidPage(selenium, base_url, locale='de').open()
    with pytest.raises(TimeoutException):
        page.send_to_device.click_send()


@pytest.mark.nondestructive
def test_send_to_device_not_supported_locale(base_url, selenium):
    page = AndroidPage(selenium, base_url, locale='it').open()
    assert page.is_play_store_button_displayed
    assert not page.send_to_device.is_displayed


@pytest.mark.skipif(reason='https://webqa-ci.mozilla.com/job/bedrock.dev.win10.ie/120/')
@pytest.mark.nondestructive
def test_open_close_accordion(base_url, selenium):
    page = AndroidPage(selenium, base_url, locale='de').open()
    sections = page.customize_sections
    assert sections[0].is_displayed
    for i in range(1, len(sections)):
        sections[i].show_detail()
        assert sections[i].is_displayed
        assert not sections[i - 1].is_displayed
    for i in range(len(sections) - 2, -1, -1):
        sections[i].show_detail()
        assert sections[i].is_displayed
        assert not sections[i + 1].is_displayed
    sections[0].hide_detail()
    assert not sections[0].is_displayed


@pytest.mark.nondestructive
def test_next_previous_buttons(base_url, selenium):
    page = AndroidPage(selenium, base_url, locale='de').open()
    sections = page.customize_sections
    for i in range(len(sections) - 1):
        assert sections[i].is_displayed
        page.show_next_customize_section()
        assert not sections[i - 1].is_displayed
    for i in range(len(sections) - 1, 0, -1):
        assert sections[i].is_displayed
        page.show_previous_customize_section()
        assert not sections[i].is_displayed
    assert sections[0].is_displayed


@pytest.mark.skipif(reason='https://webqa-ci.mozilla.com/job/bedrock.dev.win10.ie/120/')
@pytest.mark.nondestructive
@pytest.mark.viewport('mobile')
def test_mobile_accordion(base_url, selenium):
    page = AndroidPage(selenium, base_url, locale='de').open()
    sections = page.customize_sections
    assert not sections[0].is_displayed
    for i in range(len(sections)):
        sections[i].show_detail()
        assert sections[i].is_displayed
    assert all(section.is_displayed for section in sections)
    for i in range(len(sections) - 1, -1, -1):
        sections[i].hide_detail()
        assert not sections[i].is_displayed
    assert not any(section.is_displayed for section in sections)
