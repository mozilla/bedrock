# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.lockwise import LockwisePage


@pytest.mark.nondestructive
def test_mobile_buttons_are_displayed(base_url, selenium):
    page = LockwisePage(selenium, base_url).open()
    assert page.is_app_store_button_displayed
    assert page.is_play_store_button_displayed


@pytest.mark.skip_if_firefox(reason='Download button is displayed only to non-Firefox users')
@pytest.mark.nondestructive
def test_download_button_is_displayed(base_url, selenium):
    page = LockwisePage(selenium, base_url).open()
    assert page.download_button.is_displayed
