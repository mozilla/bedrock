# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.desktop.desktop import DesktopPage


@pytest.mark.nondestructive
def test_primary_download_button_displayed(base_url, selenium):
    page = DesktopPage(selenium, base_url, locale='de').open()
    page.wait_for_download_button_to_display()
    assert page.primary_download_button.is_displayed
