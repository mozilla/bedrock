# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.switch import FirefoxSwitchPage


@pytest.mark.nondestructive
def test_download_button_displayed(base_url, selenium):
    page = FirefoxSwitchPage(selenium, base_url).open()
    assert page.download_button.is_displayed
