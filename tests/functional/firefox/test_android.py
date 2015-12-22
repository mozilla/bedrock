# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.android import AndroidPage


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_family_navigation(base_url, selenium):
    page = AndroidPage(base_url, selenium).open()
    page.family_navigation.open_menu()
    assert page.family_navigation.is_menu_displayed


@pytest.mark.skipif(reason='https://webqa-ci.mozilla.com/job/bedrock.dev.win10.ie/120/')
@pytest.mark.smoke
@pytest.mark.nondestructive
def test_open_close_accordion(base_url, selenium):
    page = AndroidPage(base_url, selenium).open()
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
    page = AndroidPage(base_url, selenium).open()
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
    page = AndroidPage(base_url, selenium).open()
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
