# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.pocket import FirefoxPocketPage


@pytest.mark.nondestructive
def test_pocket_learn_more_button(base_url, selenium):
    page = FirefoxPocketPage(selenium, base_url).open()
    assert page.is_pocket_primary_button_displayed
    assert page.is_pocket_secondary_button_displayed
