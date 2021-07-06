# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.whatsnew.whatsnew_90 import FirefoxWhatsNew90Page


@pytest.mark.nondestructive
def test_get_vpn_button_is_displayed(base_url, selenium):
    page = FirefoxWhatsNew90Page(selenium, base_url, locale='de').open()
    assert page.is_get_vpn_button_displayed
