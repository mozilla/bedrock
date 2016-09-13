# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.channel.ios import ChannelIOSPage


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_download_buttons_are_displayed(base_url, selenium):
    page = ChannelIOSPage(selenium, base_url).open()
    assert page.is_testflight_button_displayed
