# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.home import HomePage


@pytest.mark.skip_if_firefox(reason='Download button is displayed only to non-Firefox users')
@pytest.mark.sanity
@pytest.mark.nondestructive
def test_download_button_is_displayed_en(base_url, selenium):
    page = HomePage(selenium, base_url).open()
    assert page.primary_download_button.is_displayed
    assert page.secondary_download_button.is_displayed


@pytest.mark.skip_if_not_firefox(reason='Firefox Accounts CTA is displayed only to Firefox users')
@pytest.mark.nondestructive
def test_accounts_button_is_displayed_en(base_url, selenium):
    page = HomePage(selenium, base_url).open()
    assert page.is_primary_accounts_button
    assert page.is_secondary_accounts_button


@pytest.mark.sanity
@pytest.mark.nondestructive
def test_download_button_is_displayed_locales(base_url, selenium):
    page = HomePage(selenium, base_url, locale='de').open()
    assert page.intro_download_button.is_displayed
