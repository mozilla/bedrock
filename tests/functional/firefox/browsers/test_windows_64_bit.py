# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.browsers.windows_64_bit import Windows64BitPage


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_download_button_is_displayed(base_url, selenium):
    page = Windows64BitPage(selenium, base_url).open()
    assert page.is_windows_64_bit_hero_download_button_displayed
    assert page.is_windows_64_bit_footer_download_button_displayed
