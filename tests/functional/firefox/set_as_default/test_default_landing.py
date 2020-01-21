# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.set_as_default.landing import DefaultLandingPage


@pytest.mark.nondestructive
def test_set_default_button_is_displayed(base_url, selenium):
    page = DefaultLandingPage(selenium, base_url).open()
    assert page.is_set_default_button_displayed
