# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.whatsnew.whatsnew_developer_70 import FirefoxWhatsNewDeveloper70Page


@pytest.mark.skip_if_not_firefox(reason="Whatsnew pages are shown to Firefox only.")
@pytest.mark.nondestructive
def test_nightly_download_button_displayed(base_url, selenium):
    page = FirefoxWhatsNewDeveloper70Page(selenium, base_url).open()
    assert page.nightly_download_button.is_displayed
