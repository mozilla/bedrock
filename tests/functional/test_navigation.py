# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.home import HomePage


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_navigation(base_url, selenium):
    page = HomePage(selenium, base_url).open()
    firefox_desktop_page = page.navigation.open_firefox_desktop_page()
    assert firefox_desktop_page.seed_url in selenium.current_url

    page.open()
    developer_edition_page = page.navigation.open_developer_edition_page()
    assert developer_edition_page.seed_url in selenium.current_url

    page.open()
    manifesto_page = page.navigation.open_manifesto_page()
    assert manifesto_page.seed_url in selenium.current_url


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_mobile_navigation(base_url, selenium_mobile):
    page = HomePage(selenium_mobile, base_url).open()
    page.navigation.show()
    firefox_desktop_page = page.navigation.open_firefox_desktop_page()
    assert firefox_desktop_page.seed_url in selenium_mobile.current_url

    page.open()
    page.navigation.show()
    developer_edition_page = page.navigation.open_developer_edition_page()
    assert developer_edition_page.seed_url in selenium_mobile.current_url

    page.open()
    page.navigation.show()
    manifesto_page = page.navigation.open_manifesto_page()
    assert manifesto_page.seed_url in selenium_mobile.current_url


@pytest.mark.smoke
@pytest.mark.nondestructive
@pytest.mark.skip_if_firefox(reason='Firefox download button is shown only to non-Firefox users.')
def test_navigation_download_firefox_button(base_url, selenium):
    page = HomePage(selenium, base_url).open()
    assert not page.navigation.is_firefox_accounts_button_displayed
    assert page.navigation.is_firefox_download_button_displayed


@pytest.mark.nondestructive
@pytest.mark.skip_if_not_firefox(reason='Firefox Accounts button is shown only to Firefox users.')
def test_navigation_firefox_account_button(base_url, selenium):
    page = HomePage(selenium, base_url).open()
    assert not page.navigation.is_firefox_download_button_displayed
    assert page.navigation.is_firefox_accounts_button_displayed
