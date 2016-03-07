# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.smarton.landing import SmartOnLandingPage


@pytest.mark.nondestructive
def test_navigation(base_url, selenium):
    page = SmartOnLandingPage(base_url, selenium).open()
    tracking_page = page.open_tracking()
    assert tracking_page.url in selenium.current_url

    page.open()
    security_page = page.open_security()
    assert security_page.url in selenium.current_url

    page.open()
    surveillance_page = page.open_surveillance()
    assert surveillance_page.url in selenium.current_url
