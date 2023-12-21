# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.products.vpn.landing_refresh import VPNLandingPage


@pytest.mark.nondestructive
def test_accept_consent_banner(base_url, selenium):
    page = VPNLandingPage(selenium, base_url, params="?geo=de").open()
    assert page.consent_banner.is_displayed
    page.consent_banner.click_accept_button()
    assert not page.consent_banner.is_displayed


@pytest.mark.nondestructive
def test_reject_consent_banner(base_url, selenium):
    page = VPNLandingPage(selenium, base_url, params="?geo=de").open()
    assert page.consent_banner.is_displayed
    page.consent_banner.click_reject_button()
    assert not page.consent_banner.is_displayed
