# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.whatsnew.whatsnew_76 import FirefoxWhatsNew76Page


@pytest.mark.skip_if_not_firefox(reason='Whatsnew pages are shown to Firefox only.')
@pytest.mark.nondestructive
def test_facebook_container_picto_block_displayed(base_url, selenium):
    page = FirefoxWhatsNew76Page(selenium, base_url, params='').open()
    assert page.is_facebook_container_picto_block_displayed
    assert page.are_three_columns_displayed
    assert not page.are_two_columns_displayed


@pytest.mark.skip_if_not_firefox(reason='Whatsnew pages are shown to Firefox only.')
@pytest.mark.nondestructive
def test_cta_button_displayed(base_url, selenium):
    page = FirefoxWhatsNew76Page(selenium, base_url, params='').open()
    assert page.is_cta_button_displayed
