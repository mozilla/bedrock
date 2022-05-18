# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.products.vpn.download import VPNDownloadPage


@pytest.mark.nondestructive
def test_vpn_download_buttons_displayed(base_url, selenium):
    page = VPNDownloadPage(selenium, base_url, params="?geo=us").open()
    assert page.is_windows_download_button_displayed
    assert page.is_mac_download_button_displayed
    assert page.is_linux_download_button_displayed
    assert page.is_android_download_button_displayed
    assert page.is_ios_download_button_displayed


@pytest.mark.nondestructive
@pytest.mark.parametrize(
    "country",
    [("cn"), ("cu"), ("ir"), ("kp"), ("sd"), ("sy")],
)
def test_vpn_download_blocked_in_country(country, base_url, selenium):
    page = VPNDownloadPage(selenium, base_url, params=f"?geo={country}").open()
    assert not page.is_windows_download_button_displayed
    assert not page.is_mac_download_button_displayed
    assert not page.is_linux_download_button_displayed
    assert not page.is_android_download_button_displayed
    assert not page.is_ios_download_button_displayed
