# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.os.tv import TVPage


@pytest.mark.sanity
@pytest.mark.nondestructive
def test_next_previous_buttons(base_url, selenium):
    page = TVPage(base_url, selenium).open()
    assert not page.is_previous_enabled
    screens = page.screens
    thumbnails = page.thumbnails
    for i in range(len(screens) - 1):
        assert screens[i].is_displayed
        assert thumbnails[i].is_selected
        page.show_next_screen()
    assert not page.is_next_enabled
    for i in range(len(screens) - 1, 0, -1):
        assert screens[i].is_displayed
        assert thumbnails[i].is_selected
        page.show_previous_screen()
    assert not page.is_previous_enabled
    assert screens[0].is_displayed
    assert thumbnails[0].is_selected


@pytest.mark.sanity
@pytest.mark.nondestructive
def test_click_thumbnails(base_url, selenium):
    page = TVPage(base_url, selenium).open()
    screens = page.screens
    thumbnails = page.thumbnails
    assert screens[0].is_displayed
    assert thumbnails[0].is_selected
    for i in range(1, len(thumbnails)):
        thumbnails[i].click()
        assert screens[i].is_displayed
        assert thumbnails[i].is_selected
    for i in range(len(thumbnails) - 2, -1, -1):
        thumbnails[i].click()
        assert screens[i].is_displayed
        assert thumbnails[i].is_selected
    assert screens[0].is_displayed
    assert thumbnails[0].is_selected
