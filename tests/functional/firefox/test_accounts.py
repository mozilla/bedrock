# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.accounts import FirefoxAccountsPage


@pytest.mark.skip_if_firefox(reason='Download button is displayed only to non-Firefox users')
@pytest.mark.nondestructive
def test_download_button_displayed(base_url, selenium):
    page = FirefoxAccountsPage(selenium, base_url).open()
    assert not page.is_accounts_form_displayed
    assert page.download_button.is_displayed


@pytest.mark.skip_if_not_firefox(reason='Accounts iFrame is only displayed to Firefox users')
@pytest.mark.nondestructive
def test_accounts_form_displayed(base_url, selenium):
    page = FirefoxAccountsPage(selenium, base_url).open()
    assert not page.download_button.is_displayed
    assert page.is_accounts_form_displayed
