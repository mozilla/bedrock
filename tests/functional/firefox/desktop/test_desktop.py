# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.desktop.desktop import DesktopPage


@pytest.mark.skip_if_firefox
@pytest.mark.smoke
@pytest.mark.nondestructive
def test_primary_download_button_displayed(base_url, selenium):
    page = DesktopPage(base_url, selenium).open()
    assert page.primary_download_button.is_displayed
