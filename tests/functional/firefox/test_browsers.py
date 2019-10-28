# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from urllib.parse import unquote

from pages.firefox.browsers import FirefoxBrowsersPage


@pytest.mark.nondestructive
def test_primary_download_button_displayed(base_url, selenium):
    page = FirefoxBrowsersPage(selenium, base_url).open()
    assert page.is_primary_download_button_displayed


@pytest.mark.nondestructive
def test_account_form(base_url, selenium):
    page = FirefoxBrowsersPage(selenium, base_url, params='').open()
    page.join_firefox_form.type_email('success@example.com')
    page.join_firefox_form.click_continue()
    url = unquote(selenium.current_url)
    assert 'email=success@example.com' in url, 'Email address is not in URL'
