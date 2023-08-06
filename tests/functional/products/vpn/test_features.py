# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.products.vpn.features import VPNFeaturesPage


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
    page = VPNFeaturesPage(selenium, base_url, params=f"?geo={country}").open()
    # Footer
    assert not page.is_join_waitlist_footer_button_displayed
    assert page.is_get_vpn_footer_button_displayed


@pytest.mark.nondestructive
def test_vpn_not_available_in_country(base_url, selenium):
    page = VPNFeaturesPage(selenium, base_url, params="?geo=cn").open()
    # Footer
    assert page.is_join_waitlist_footer_button_displayed
    assert not page.is_get_vpn_footer_button_displayed
