# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.accounts import FirefoxAccountsPage


@pytest.mark.nondestructive
def test_account_form(base_url, selenium):
    page = FirefoxAccountsPage(selenium, base_url).open()
    assert page.is_create_account_form_displayed, "Create account form is displayed for signed out users"
