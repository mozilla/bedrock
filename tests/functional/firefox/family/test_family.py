# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.family.landing import FamilyPage


@pytest.mark.skip_if_firefox(reason="Nav download button is displayed only to non-Firefox users")
def test_firefox_nav_download_button_is_displayed(base_url, selenium):
    page = FamilyPage(selenium, base_url).open()
    assert page.is_firefox_nav_download_button_displayed


@pytest.mark.skip_if_not_firefox(reason="Nav CTA is only hidden for Firefox users")
def test_firefox_nav_cta_is_displayed(base_url, selenium):
    page = FamilyPage(selenium, base_url).open()
    assert not page.is_firefox_nav_cta_displayed


@pytest.mark.skip_if_firefox(reason="Download CTA is only shown for non-Firefox users")
def test_firefox_desktop_download_button_is_displayed(base_url, selenium):
    page = FamilyPage(selenium, base_url).open()
    assert page.is_firefox_desktop_download_button_displayed
    assert not page.is_firefox_make_default_button_displayed


@pytest.mark.skip_if_not_firefox(reason="Make Default CTA is only shown for (non-default) Firefox users")
def test_firefox_make_default_button_is_displayed(base_url, selenium):
    page = FamilyPage(selenium, base_url).open()
    assert page.is_firefox_make_default_button_displayed
    assert not page.is_firefox_desktop_download_button_displayed


def test_firefox_pdf_download_button_is_displayed(base_url, selenium):
    page = FamilyPage(selenium, base_url).open()
    assert page.is_firefox_pdf_download_button_displayed
