# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.facebook_container import FacebookContainerPage


@pytest.mark.skip_if_not_firefox(reason='Addon link is shown only to Firefox users.')
@pytest.mark.nondestructive
def test_facebook_container_link_is_displayed(base_url, selenium):
    page = FacebookContainerPage(selenium, base_url).open()
    assert page.is_facebook_container_link_displayed


@pytest.mark.skip_if_firefox(reason='Firefox download button is shown only to non-Firefox users.')
@pytest.mark.nondestructive
def test_firefox_download_button_is_displayed(base_url, selenium):
    page = FacebookContainerPage(selenium, base_url).open()
    assert page.firefox_download_button.is_displayed
