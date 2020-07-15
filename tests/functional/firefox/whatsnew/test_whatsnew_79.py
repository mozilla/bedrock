# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.whatsnew.whatsnew_79 import FirefoxWhatsNew79Page


@pytest.mark.skip_if_not_firefox(reason='Whatsnew pages are shown to Firefox only.')
@pytest.mark.nondestructive
def test_default_browser_button_is_displayed(base_url, selenium):
    page = FirefoxWhatsNew79Page(selenium, base_url, params='').open()
    assert page.is_default_browser_button_displayed
