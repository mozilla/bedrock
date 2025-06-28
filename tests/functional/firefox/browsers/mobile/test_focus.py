# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from bedrock import settings
from pages.firefox.browsers.mobile_focus import FirefoxMobileFocusPage


@pytest.mark.skipif(
    settings.ENABLE_FIREFOX_COM_REDIRECTS is True,
    reason="Related view is now unreachable and [TODO] should be removed",
)
@pytest.mark.smoke
@pytest.mark.nondestructive
def test_get_firefox_qr_code(base_url, selenium):
    page = FirefoxMobileFocusPage(selenium, base_url, locale="en-US").open()
    assert page.is_firefox_qr_code_displayed
