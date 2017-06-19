# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.android_hub import FirefoxAndroidHubPage


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_play_store_button_is_displayed(base_url, selenium):
    page = FirefoxAndroidHubPage(selenium, base_url).open()
    assert page.is_play_store_button_displayed
