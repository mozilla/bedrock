# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.whatsnew.whatsnew_95 import FirefoxWhatsNew95Page


@pytest.mark.skip_if_not_firefox(reason="Whatsnew pages are shown to Firefox only.")
@pytest.mark.nondestructive
def test_pocket_buttons_are_displayed(base_url, selenium):
    page = FirefoxWhatsNew95Page(selenium, base_url, locale="de").open()
    assert page.is_pocket_button_displayed
