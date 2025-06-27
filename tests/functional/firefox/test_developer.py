# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from bedrock import settings
from pages.firefox.developer import DeveloperPage


@pytest.mark.skipif(
    settings.ENABLE_FIREFOX_COM_REDIRECTS is True,
    reason="Related view is now unreachable and [TODO] should be removed",
)
@pytest.mark.smoke
@pytest.mark.nondestructive
def test_download_buttons_are_displayed(base_url, selenium):
    page = DeveloperPage(selenium, base_url).open()
    assert page.primary_download_button.is_displayed
    assert page.secondary_download_button.is_displayed
