# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.accounts_features import AccountsFeaturesPage


@pytest.mark.skip_if_not_firefox(reason='Create Account button is shown only to Firefox users.')
@pytest.mark.nondestructive
def test_is_create_account_button_displayed(base_url, selenium):
    page = AccountsFeaturesPage(selenium, base_url).open()
    assert page.is_create_account_button_displayed


@pytest.mark.skip_if_firefox(reason='Download button is shown only to non-Firefox users.')
@pytest.mark.nondestructive
def test_is_download_button_displayed(base_url, selenium):
    page = AccountsFeaturesPage(selenium, base_url).open()
    assert page.download_button.is_displayed
