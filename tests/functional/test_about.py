# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.about import AboutPage


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_read_mission_button_displayed(base_url, selenium):
    page = AboutPage(selenium, base_url).open()
    assert page.is_read_mission_button_displayed
