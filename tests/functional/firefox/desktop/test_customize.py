# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.desktop.customize import CustomizePage


@pytest.mark.nondestructive
def test_customizer_click_nav_links(base_url, selenium):
    page = CustomizePage(base_url, selenium).open()
    links = page.customize_links
    sections = page.customize_sections
    assert sections[0].is_displayed
    assert links[0].is_selected
    for i in range(1, len(links)):
        links[i].click()
        assert links[i].is_selected
        assert sections[i].is_displayed


@pytest.mark.nondestructive
def test_customizer_click_next(base_url, selenium):
    page = CustomizePage(base_url, selenium).open()
    sections = page.customize_sections
    assert sections[0].is_displayed
    for i in range(len(sections)):
        assert sections[i].is_displayed
        sections[i].click_next()
    assert sections[0].is_displayed


@pytest.mark.nondestructive
def test_theme_buttons(base_url, selenium):
    page = CustomizePage(base_url, selenium).open()
    themes = page.themes
    assert themes[-1].is_selected
    assert themes[-1].is_image_displayed
    for i in range(len(themes) - 2, -1, -1):
        themes[i].click_button()
        assert themes[i].is_selected
        assert themes[i].is_image_displayed


@pytest.mark.nondestructive
def test_sync_button_displayed(base_url, selenium):
    page = CustomizePage(base_url, selenium).open()
    assert page.is_sync_button_displayed
