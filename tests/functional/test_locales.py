# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.locales import LocalesPage


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_locales_are_displayed(base_url, selenium):
    page = LocalesPage(selenium, base_url).open()
    assert page.number_of_america_locales > 1
    assert page.number_of_asia_pacific_locales > 1
    assert page.number_of_europe_locales > 1
    assert page.number_of_middle_east_locales > 1
