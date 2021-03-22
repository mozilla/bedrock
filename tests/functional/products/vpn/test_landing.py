# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.products.vpn.landing import VPNLandingPage


@pytest.mark.nondestructive
def test_vpn_available_in_country(base_url, selenium):
    page = VPNLandingPage(selenium, base_url, params='?geo=us').open()
    assert page.is_get_vpn_hero_fixed_price_button_displayed
    assert not page.is_join_waitlist_hero_button_displayed
    assert page.is_get_vpn_navigation_fixed_price_button_displayed
    assert not page.is_join_waitlist_navigation_button_displayed
    assert page.is_get_vpn_conntect_now_fixed_price_button_displayed
    assert not page.is_join_waitlist_coming_soon_button_displayed
    assert page.is_get_vpn_fixed_pricing_section_button_displayed
    assert not page.is_join_waitlist_fixed_pricing_section_button_displayed
    assert page.is_get_vpn_footer_fixed_price_button_displayed
    assert not page.is_join_waitlist_footer_button_displayed


@pytest.mark.nondestructive
def test_vpn_not_available_in_country(base_url, selenium):
    page = VPNLandingPage(selenium, base_url, params='?geo=cn').open()
    assert not page.is_get_vpn_hero_fixed_price_button_displayed
    assert page.is_join_waitlist_hero_button_displayed
    assert not page.is_get_vpn_navigation_fixed_price_button_displayed
    assert page.is_join_waitlist_navigation_button_displayed
    assert not page.is_get_vpn_conntect_now_fixed_price_button_displayed
    assert page.is_join_waitlist_coming_soon_button_displayed
    assert not page.is_get_vpn_fixed_pricing_section_button_displayed
    assert page.is_join_waitlist_fixed_pricing_section_button_displayed
    assert not page.is_get_vpn_footer_fixed_price_button_displayed
    assert page.is_join_waitlist_footer_button_displayed
