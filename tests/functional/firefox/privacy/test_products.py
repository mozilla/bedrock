# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.privacy.products import FirefoxPrivacyProductsPage


@pytest.mark.smoke
@pytest.mark.skip_if_firefox(reason='Download buttons are shown to non-Firefox browsers only')
@pytest.mark.nondestructive
def test_download_button_displayed(base_url, selenium):
    page = FirefoxPrivacyProductsPage(selenium, base_url, params='').open()
    assert page.primary_download_button.is_displayed
    assert page.secondary_download_button.is_displayed
