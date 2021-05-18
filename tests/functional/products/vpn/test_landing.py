# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.products.vpn.landing import VPNLandingPage


@pytest.mark.skip(reason='Skipped until variable pricing for wave 1 countries is enabled: issue 10199.')
@pytest.mark.nondestructive
@pytest.mark.parametrize('country', [('us'), ('ca'), ('my'), ('nz'), ('sg'), ('gb')])
def test_vpn_fixed_price_available_in_country(country, base_url, selenium):
    page = VPNLandingPage(selenium, base_url, params='?geo={0}'.format(country)).open()
    # Hero
    assert page.is_get_vpn_hero_fixed_price_button_displayed
    assert not page.is_join_waitlist_hero_button_displayed
    assert not page.is_get_vpn_hero_variable_price_anchor_displayed

    # Navigation
    assert page.is_get_vpn_navigation_fixed_price_button_displayed
    assert not page.is_join_waitlist_navigation_button_displayed
    assert not page.is_get_vpn_navigation_variable_price_anchor_displayed

    # Connect section
    assert page.is_get_vpn_conntect_now_fixed_price_button_displayed
    assert not page.is_join_waitlist_coming_soon_button_displayed
    assert not page.is_get_vpn_conntect_now_variable_price_anchor_displayed

    # Pricing section
    assert page.is_get_vpn_fixed_price_section_button_displayed
    assert not page.is_join_waitlist_fixed_price_section_button_displayed
    assert not page.is_get_vpn_vpn_variable_price_monthly_button_displayed
    assert not page.is_get_vpn_vpn_variable_price_6_months_button_displayed
    assert not page.is_get_vpn_vpn_variable_price_12_months_button_displayed

    # Footer
    assert page.is_get_vpn_footer_fixed_price_button_displayed
    assert not page.is_join_waitlist_footer_button_displayed
    assert not page.is_get_vpn_footer_variable_price_anchor_displayed


@pytest.mark.nondestructive
@pytest.mark.parametrize('country', [('de'), ('fr')])
def test_vpn_variable_price_available_in_country(country, base_url, selenium):
    page = VPNLandingPage(selenium, base_url, params='?geo={0}'.format(country)).open()
    # Hero
    assert not page.is_get_vpn_hero_fixed_price_button_displayed
    assert not page.is_join_waitlist_hero_button_displayed
    assert page.is_get_vpn_hero_variable_price_anchor_displayed

    # Navigation
    assert not page.is_get_vpn_navigation_fixed_price_button_displayed
    assert not page.is_join_waitlist_navigation_button_displayed
    assert page.is_get_vpn_navigation_variable_price_anchor_displayed

    # Connect section
    assert not page.is_get_vpn_conntect_now_fixed_price_button_displayed
    assert not page.is_join_waitlist_coming_soon_button_displayed
    assert page.is_get_vpn_conntect_now_variable_price_anchor_displayed

    # Pricing section
    assert not page.is_get_vpn_fixed_price_section_button_displayed
    assert not page.is_join_waitlist_fixed_price_section_button_displayed
    assert page.is_get_vpn_vpn_variable_price_monthly_button_displayed
    assert page.is_get_vpn_vpn_variable_price_6_months_button_displayed
    assert page.is_get_vpn_vpn_variable_price_12_months_button_displayed

    # Footer
    assert not page.is_get_vpn_footer_fixed_price_button_displayed
    assert not page.is_join_waitlist_footer_button_displayed
    assert page.is_get_vpn_footer_variable_price_anchor_displayed


@pytest.mark.nondestructive
def test_vpn_not_available_in_country(base_url, selenium):
    page = VPNLandingPage(selenium, base_url, params='?geo=cn').open()
    # Hero
    assert not page.is_get_vpn_hero_fixed_price_button_displayed
    assert page.is_join_waitlist_hero_button_displayed
    assert not page.is_get_vpn_hero_variable_price_anchor_displayed

    # Navigation
    assert not page.is_get_vpn_navigation_fixed_price_button_displayed
    assert page.is_join_waitlist_navigation_button_displayed
    assert not page.is_get_vpn_navigation_variable_price_anchor_displayed

    # Connect section
    assert not page.is_get_vpn_conntect_now_fixed_price_button_displayed
    assert page.is_join_waitlist_coming_soon_button_displayed
    assert not page.is_get_vpn_conntect_now_variable_price_anchor_displayed

    # Pricing section
    assert not page.is_get_vpn_fixed_price_section_button_displayed
    assert page.is_join_waitlist_fixed_price_section_button_displayed
    assert not page.is_get_vpn_vpn_variable_price_monthly_button_displayed
    assert not page.is_get_vpn_vpn_variable_price_6_months_button_displayed
    assert not page.is_get_vpn_vpn_variable_price_12_months_button_displayed

    # Footer
    assert not page.is_get_vpn_footer_fixed_price_button_displayed
    assert page.is_join_waitlist_footer_button_displayed
    assert not page.is_get_vpn_footer_variable_price_anchor_displayed
