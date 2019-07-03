# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.history import HistoryPage


@pytest.mark.nondestructive
def test_slideshow_displayed(base_url, selenium):
    page = HistoryPage(selenium, base_url).open()
    assert page.is_slideshow_displayed
    assert page.is_previous_button_displayed
    assert page.is_next_button_displayed


@pytest.mark.nondestructive
def test_list_displayed(base_url, selenium_mobile):
    page = HistoryPage(selenium_mobile, base_url).open()
    assert not page.is_slideshow_displayed
    assert not page.is_previous_button_displayed
    assert not page.is_next_button_displayed
