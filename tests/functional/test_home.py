# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.home import HomePage


@pytest.mark.skip_if_firefox(reason='Download button is displayed only to non-Firefox users')
@pytest.mark.sanity
@pytest.mark.smoke
@pytest.mark.nondestructive
@pytest.mark.parametrize('locale', ['en-US', 'de', 'fr', 'es-ES'])
def test_download_button_is_displayed(locale, base_url, selenium):
    page = HomePage(selenium, base_url, locale=locale).open()
    assert page.is_primary_download_button_displayed
    assert page.is_secondary_download_button_displayed


@pytest.mark.skip_if_not_firefox(reason='Alternative CTA is displayed only to Firefox users')
@pytest.mark.nondestructive
def test_accounts_button_is_displayed(base_url, selenium):
    page = HomePage(selenium, base_url, locale='en-US').open()
    assert page.is_primary_alt_button_displayed
    assert page.is_secondary_accounts_button_displayed
    assert not page.is_primary_download_button_displayed
    assert not page.is_secondary_download_button_displayed
