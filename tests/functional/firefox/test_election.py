# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.election import ElectionPage


@pytest.mark.skip_if_not_firefox(reason='Extension buttons are shown only to Firefox users')
@pytest.mark.nondestructive
def test_extension_buttons_are_displayed(base_url, selenium):
    page = ElectionPage(selenium, base_url).open()
    assert page.is_facebook_container_button_displayed
    assert page.is_pro_republica_button_displayed


@pytest.mark.skip_if_firefox(reason='Funnelcake download button shown only to non-Firefox users')
@pytest.mark.nondestructive
def test_funnelcake_button_is_displayed(base_url, selenium):
    page = ElectionPage(selenium, base_url).open()
    assert page.is_funnelcake_download_button_displayed
