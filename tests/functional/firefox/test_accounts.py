# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.accounts import FirefoxAccountsPage


# test Firefox state
@pytest.mark.skip_if_not_firefox(reason='Non-Firefox user does not see Firefox state')
@pytest.mark.nondestructive
def test_firefox_state(base_url, selenium):
    page = FirefoxAccountsPage(selenium, base_url).open()
    assert not page.are_download_buttons_displayed, "Download buttons are displayed for Firefox user"
    assert page.is_create_account_form_displayed, "Create account form is not displayed for Firefox user"


# test non-Firefox state
@pytest.mark.skip_if_firefox(reason='Firefox user does not see non-Firefox state')
@pytest.mark.nondestructive
def test_non_firefox_state(base_url, selenium):
    page = FirefoxAccountsPage(selenium, base_url).open()
    assert page.are_download_buttons_displayed, "Download buttons are not displayed for non-Firefox user"
    assert not page.is_create_account_form_displayed, "Create account form is displayed for non-Firefox user"
