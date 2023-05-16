# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.products.vpn.pricing import VPNPricingPage


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
        ("bg"),
        ("cy"),
        ("cz"),
        ("dk"),
        ("ee"),
        ("hr"),
        ("hu"),
        ("lt"),
        ("lu"),
        ("lv"),
        ("mt"),
        ("pl"),
        ("pt"),
        ("ro"),
        ("si"),
        ("sk"),
    ],
)
def test_vpn_pricing_available_in_country(country, base_url, selenium):
    page = VPNPricingPage(selenium, base_url, params=f"?geo={country}").open()
    assert page.is_get_vpn_monthly_button_displayed
    assert page.is_get_vpn_12_months_button_displayed
    assert not page.is_join_waitlist_button_displayed


@pytest.mark.nondestructive
def test_vpn_pricing_not_available_in_country(base_url, selenium):
    page = VPNPricingPage(selenium, base_url, params="?geo=cn").open()
    assert not page.is_get_vpn_monthly_button_displayed
    assert not page.is_get_vpn_12_months_button_displayed
    assert page.is_join_waitlist_button_displayed
