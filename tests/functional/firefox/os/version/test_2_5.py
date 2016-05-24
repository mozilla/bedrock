# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.os.os import FirefoxOSPage


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_download_buttons_are_displayed(base_url, selenium):
    page = FirefoxOSPage(selenium, base_url).open()
    assert page.is_primary_download_button_displayed
    assert page.is_secondary_download_button_displayed
