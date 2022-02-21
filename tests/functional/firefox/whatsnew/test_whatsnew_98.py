# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.whatsnew.whatsnew_98 import FirefoxWhatsNew98Page


@pytest.mark.skip_if_not_firefox(reason="Whatsnew pages are shown to Firefox only.")
@pytest.mark.nondestructive
@pytest.mark.parametrize("country", [("se"), ("fi")])
def test_vpn_button_is_displayed(country, base_url, selenium):
    page = FirefoxWhatsNew98Page(selenium, base_url, locale="en-US", params=f"?geo={country}").open()
    assert page.is_vpn_button_displayed
