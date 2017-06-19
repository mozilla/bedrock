# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.desktop.hub import FirefoxDesktopHubPage


@pytest.mark.smoke
@pytest.mark.sanity
@pytest.mark.nondestructive
def test_download_buttons_displayed(base_url, selenium):
    page = FirefoxDesktopHubPage(selenium, base_url).open()
    assert page.download_button.is_displayed
