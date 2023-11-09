# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.products.vpn.landing import VPNLandingPage


@pytest.mark.nondestructive
@pytest.mark.parametrize(
    "country",
    [
        ("us"),
        ("ca"),
        ("my"),
        ("nz"),
        ("sg"),
        ("gb"),
        ("de"),
        ("fr"),
        ("at"),
        ("be"),
        ("ch"),
        ("es"),
        ("it"),
        ("ie"),
        ("nl"),
        ("se"),
        ("fi"),
    ],
)
def test_vpn_available_in_country(country, base_url, selenium):
    page = VPNLandingPage(selenium, base_url, locale="de", params=f"?xv=legacy&geo={country}").open()
    # Hero
    assert not page.is_join_waitlist_hero_button_displayed
    assert page.is_get_vpn_hero_button_displayed

    # Navigation
    assert not page.is_join_waitlist_navigation_button_displayed
    assert page.is_get_vpn_navigation_button_displayed

    # Pricing section
    assert page.is_get_vpn_monthly_button_displayed
    assert page.is_get_vpn_12_months_button_displayed

    # VPN + Relay bundle is only available in US & Canada.
    # Currently disabled in production behind a switch.
    # if country in ["us", "ca"]:
    #     assert page.is_get_vpn_relay_button_displayed
    # else:
    #     assert not page.is_get_vpn_relay_button_displayed

    # Waitlist features section
    assert not page.is_join_waitlist_features_button_displayed

    # Connect section
    assert not page.is_join_waitlist_coming_soon_button_displayed
    assert page.is_get_vpn_conntect_now_button_displayed

    # Footer
    assert not page.is_join_waitlist_footer_button_displayed
    assert page.is_get_vpn_footer_button_displayed


@pytest.mark.nondestructive
def test_vpn_not_available_in_country(base_url, selenium):
    page = VPNLandingPage(selenium, base_url, locale="de", params="?xv=legacy&geo=cn").open()
    # Hero
    assert page.is_join_waitlist_hero_button_displayed
    assert not page.is_get_vpn_hero_button_displayed

    # Navigation
    assert page.is_join_waitlist_navigation_button_displayed
    assert not page.is_get_vpn_navigation_button_displayed

    # Pricing section
    assert not page.is_get_vpn_monthly_button_displayed
    assert not page.is_get_vpn_12_months_button_displayed
    assert not page.is_get_vpn_relay_button_displayed

    # Waitlist features section
    assert page.is_join_waitlist_features_button_displayed

    # Connect section
    assert page.is_join_waitlist_coming_soon_button_displayed
    assert not page.is_get_vpn_conntect_now_button_displayed

    # Footer
    assert page.is_join_waitlist_footer_button_displayed
    assert not page.is_get_vpn_footer_button_displayed
