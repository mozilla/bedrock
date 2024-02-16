# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.pocket.add import AddPage

pytestmark = pytest.mark.pocket_mode


@pytest.mark.nondestructive
def test_mobile_menu(pocket_base_url, selenium_mobile):
    page = AddPage(selenium_mobile, pocket_base_url).open()
    assert page.navigation.mobile_nav_not_available
