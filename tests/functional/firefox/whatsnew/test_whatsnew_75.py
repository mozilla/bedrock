# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.whatsnew.whatsnew_75 import FirefoxWhatsNew75Page


@pytest.mark.skip_if_not_firefox(reason='Whatsnew pages are shown to Firefox only.')
@pytest.mark.nondestructive
def test_signed_out_sync_button_displayed(base_url, selenium):
    page = FirefoxWhatsNew75Page(selenium, base_url, params='').open()
    assert page.is_signed_out_sync_button_displayed


@pytest.mark.skip_if_not_firefox(reason='Whatsnew pages are shown to Firefox only.')
@pytest.mark.nondestructive
def test_signed_in_monitor_button_displayed(base_url, selenium):
    page = FirefoxWhatsNew75Page(selenium, base_url, params='?has-devices=true').open()
    assert page.is_signed_in_monitor_button_displayed


@pytest.mark.skip_if_not_firefox(reason='Whatsnew pages are shown to Firefox only.')
@pytest.mark.nondestructive
def test_signed_in_connect_device_button_displayed(base_url, selenium):
    page = FirefoxWhatsNew75Page(selenium, base_url, params='?has-no-devices=true').open()
    assert page.is_signed_in_connect_device_button_displayed
