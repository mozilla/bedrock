# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.whatsnew.whatsnew_67_0_5 import FirefoxWhatsNew6705Page


@pytest.mark.skip_if_not_firefox(reason='Whatsnew pages are shown to Firefox only.')
@pytest.mark.nondestructive
def test_signed_out_firefox_accounts_form_displayed(base_url, selenium):
    page = FirefoxWhatsNew6705Page(selenium, base_url, params='').open()
    assert page.is_firefox_accounts_form_displayed


@pytest.mark.skip_if_not_firefox(reason='Whatsnew pages are shown to Firefox only.')
@pytest.mark.nondestructive
def test_signed_in_monitor_button_displayed(base_url, selenium):
    page = FirefoxWhatsNew6705Page(selenium, base_url, params='?signed-in=true').open()
    assert page.is_monitor_button_displayed
