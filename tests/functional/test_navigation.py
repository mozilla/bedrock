# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.home import HomePage


@pytest.mark.skipif(reason='https://bugzilla.mozilla.org/show_bug.cgi?id=1214038')
@pytest.mark.nondestructive
def test_navigation(base_url, selenium):
    page = HomePage(base_url, selenium).open()
    about_page = page.navigation.open_about()
    assert about_page.url in selenium.current_url

    page.open()
    participate_page = page.navigation.open_participate()
    assert participate_page.url in selenium.current_url

    page.open()
    firefox_page = page.navigation.open_firefox()
    assert firefox_page.url in selenium.current_url


@pytest.mark.skipif(reason='https://bugzilla.mozilla.org/show_bug.cgi?id=1214038')
@pytest.mark.sanity
@pytest.mark.nondestructive
@pytest.mark.viewport('mobile')
def test_mobile_navigation(base_url, selenium):
    page = HomePage(base_url, selenium).open()
    page.navigation.show()
    about_page = page.navigation.open_about()
    assert about_page.url in selenium.current_url

    page.open().navigation.show()
    participate_page = page.navigation.open_participate()
    assert participate_page.url in selenium.current_url

    page.open().navigation.show()
    firefox_page = page.navigation.open_firefox()
    assert firefox_page.url in selenium.current_url
