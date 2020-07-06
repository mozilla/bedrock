# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.browsers.compare import BrowserComparisonPage


@pytest.mark.nondestructive
@pytest.mark.parametrize('slug', [
    ('/chrome/'),
    ('/edge/'),
    ('/safari/'),
    ('/opera/'),
    ('/brave/'),
    ('/ie/')])
def test_download_buttons_is_displayed(slug, base_url, selenium):
    page = BrowserComparisonPage(selenium, base_url, slug=slug).open()
    assert page.secondary_download_button.is_displayed


@pytest.mark.nondestructive
@pytest.mark.parametrize('slug', [
    ('/chrome/'),
    ('/edge/'),
    ('/safari/'),
    ('/opera/'),
    ('/brave/'),
    ('/ie/')])
def test_browser_menu_list_is_open(slug, base_url, selenium):
    page = BrowserComparisonPage(selenium, base_url, slug=slug).open()
    page.browser_menu_list.click()
    assert page.browser_menu_list.list_is_open
