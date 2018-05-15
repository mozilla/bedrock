# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.enterprise import EnterprisePage


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_signup_button_is_displayed(base_url, selenium):
    page = EnterprisePage(selenium, base_url).open()
    assert page.signup_button.is_displayed


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_download_links_are_displayed(base_url, selenium):
    page = EnterprisePage(selenium, base_url).open()
    assert page.download_release_link.is_displayed
    assert page.download_esr_link.is_displayed
