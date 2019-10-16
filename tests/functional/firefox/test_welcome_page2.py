# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.welcome.page2 import FirefoxWelcomePage2


@pytest.mark.nondestructive
def test_pocket_button_displayed(base_url, selenium):
    page = FirefoxWelcomePage2(selenium, base_url).open()
    assert page.is_pocket_button_displayed
