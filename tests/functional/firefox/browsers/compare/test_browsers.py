# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.browsers.compare import BrowserComparisonPage


@pytest.mark.nondestructive
@pytest.mark.parametrize("slug", [("chrome"), ("edge"), ("safari"), ("opera"), ("brave")])
def test_menu_list_is_displayed(slug, base_url, selenium):
    page = BrowserComparisonPage(selenium, base_url, slug=slug).open()
    page.browser_menu_list.click()
    assert page.browser_menu_list.list_is_open


@pytest.mark.skip_if_firefox(reason="Download button only visible to non-Firefox users")
@pytest.mark.nondestructive
@pytest.mark.parametrize("slug", [("chrome"), ("edge"), ("safari"), ("opera"), ("brave")])
def test_download_buttons_are_displayed(slug, base_url, selenium):
    page = BrowserComparisonPage(selenium, base_url, slug=slug).open()
    assert page.primary_download_button.is_displayed
    assert page.secondary_download_button.is_displayed
