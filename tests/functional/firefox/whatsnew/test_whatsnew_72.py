# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.whatsnew.whatsnew_72 import FirefoxWhatsNew72Page


@pytest.mark.skip_if_not_firefox(reason='Whatsnew pages are shown to Firefox only.')
@pytest.mark.nondestructive
def test_account_buttons_displayed(base_url, selenium):
    page = FirefoxWhatsNew72Page(selenium, base_url, params='').open()
    assert page.is_primary_account_button_displayed
    assert page.is_secondary_account_button_displayed
