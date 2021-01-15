# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.browsers.incognito_browser import IncognitoBrowserPage


@pytest.mark.nondestructive
@pytest.mark.skip_if_firefox(reason='Primary download button shown only to Firefox users.')
def test_download_buttons_are_displayed(base_url, selenium):
    page = IncognitoBrowserPage(selenium, base_url).open()
    assert page.primary_download_button.is_displayed
    assert page.secondary_download_button.is_displayed
