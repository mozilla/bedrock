# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.tiles import FirefoxTilesPage


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_family_navigation(base_url, selenium):
    page = FirefoxTilesPage(base_url, selenium).open()
    page.family_navigation.open_menu()
    assert page.family_navigation.is_menu_displayed
