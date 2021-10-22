# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.welcome.page1 import FirefoxWelcomePage1


@pytest.mark.skip_if_not_firefox(reason="Welcome pages are shown to Firefox only.")
@pytest.mark.nondestructive
def test_monitor_button_displayed(base_url, selenium):
    page = FirefoxWelcomePage1(selenium, base_url).open()
    assert page.is_primary_monitor_button_displayed
    assert page.is_secondary_monitor_button_displayed
