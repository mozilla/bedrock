# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.whatsnew.whatsnew_70 import FirefoxWhatsNew70Page


@pytest.mark.skip(reason='https://github.com/mozilla/bedrock/issues/8033')
@pytest.mark.skip_if_not_firefox(reason='Whatsnew pages are shown to Firefox only.')
@pytest.mark.nondestructive
def test_signed_out_monitor_button_displayed(base_url, selenium):
    page = FirefoxWhatsNew70Page(selenium, base_url, params='').open()
    assert page.is_signed_out_monitor_button_displayed


@pytest.mark.skip(reason='https://github.com/mozilla/bedrock/issues/8033')
@pytest.mark.skip_if_not_firefox(reason='Whatsnew pages are shown to Firefox only.')
@pytest.mark.nondestructive
def test_signed_in_monitor_button_displayed(base_url, selenium):
    page = FirefoxWhatsNew70Page(selenium, base_url, params='?signed-in=true').open()
    assert page.is_signed_in_monitor_button_displayed
