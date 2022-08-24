# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.family.landing import FamilyPage


# confirm if download button is actual download or link to download page
@pytest.mark.skip_if_firefox(reason="Download button is displayed only to non-Firefox users")
def test_firefox_download_button_is_displayed(base_url, selenium):
    page = FamilyPage(selenium, base_url).open()
    assert page.is_firefox_download_button_displayed


def test_firefox_pdf_download_button_is_displayed(base_url, selenium):
    page = CampaignFamiliesPage(selenium, base_url).open()
    assert page.is_firefox_pdf_download_button_displayed
