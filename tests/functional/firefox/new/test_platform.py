# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.new.platform import PlatformDownloadPage


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_windows_download_buttons_is_displayed(base_url, selenium):
    page = PlatformDownloadPage(selenium, base_url, slug="windows").open()
    assert page.is_windows_download_button_displayed


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_mac_download_buttons_is_displayed(base_url, selenium):
    page = PlatformDownloadPage(selenium, base_url, slug="mac").open()
    assert page.is_mac_download_button_displayed


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_linux_download_buttons_is_displayed(base_url, selenium):
    page = PlatformDownloadPage(selenium, base_url, slug="linux").open()
    assert page.is_linux64_download_button_displayed or page.is_linux_download_button_displayed
