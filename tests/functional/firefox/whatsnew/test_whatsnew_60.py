# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.whatsnew.whatsnew_60 import FirefoxWhatsNew60Page


@pytest.mark.skip_if_not_firefox(reason='Whatsnew pages are shown to Firefox only.')
@pytest.mark.nondestructive
def test_account_buttons_displayed(base_url, selenium):
    page = FirefoxWhatsNew60Page(selenium, base_url, params='').open()
    assert page.is_account_button_displayed
