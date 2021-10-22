# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.whatsnew.whatsnew_91 import FirefoxWhatsNew91Page


@pytest.mark.skip_if_not_firefox(reason="Whatsnew pages are shown to Firefox only.")
@pytest.mark.nondestructive
def test_pocket_button_is_displayed_en(base_url, selenium):
    page = FirefoxWhatsNew91Page(selenium, base_url, locale="en-US").open()
    assert page.is_pocket_primary_button_displayed
    assert page.is_pocket_secondary_button_displayed


@pytest.mark.skip_if_not_firefox(reason="Whatsnew pages are shown to Firefox only.")
@pytest.mark.nondestructive
def test_pocket_button_is_displayed_de(base_url, selenium):
    page = FirefoxWhatsNew91Page(selenium, base_url, locale="de").open()
    assert page.is_pocket_primary_button_displayed
    assert page.is_pocket_secondary_button_displayed
