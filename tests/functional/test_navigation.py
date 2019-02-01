# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.home import HomePage


@pytest.mark.nondestructive
def test_navigation(base_url, selenium):
    page = HomePage(selenium, base_url).open()
    firefox_desktop_page = page.navigation.open_firefox_desktop_page()
    assert firefox_desktop_page.seed_url in selenium.current_url

    page.open()
    developer_edition_page = page.navigation.open_developer_edition_page()
    assert developer_edition_page.seed_url in selenium.current_url

    page.open()
    about_page = page.navigation.open_about_page()
    assert about_page.seed_url in selenium.current_url


@pytest.mark.nondestructive
@pytest.mark.viewport('mobile')
def test_mobile_navigation(base_url, selenium):
    page = HomePage(selenium, base_url).open()
    page.navigation.show()
    firefox_desktop_page = page.navigation.open_firefox_desktop_page()
    assert firefox_desktop_page.seed_url in selenium.current_url

    page.open()
    page.navigation.show()
    developer_edition_page = page.navigation.open_developer_edition_page()
    assert developer_edition_page.seed_url in selenium.current_url

    page.open()
    page.navigation.show()
    about_page = page.navigation.open_about_page()
    assert about_page.seed_url in selenium.current_url
