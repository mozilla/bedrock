# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from bedrock import settings
from pages.firefox.all import FirefoxAllPage

# help modals


@pytest.mark.skipif(
    settings.ENABLE_FIREFOX_COM_REDIRECTS is True,
    reason="Related view is now unreachable and [TODO] should be removed",
)
@pytest.mark.smoke
@pytest.mark.nondestructive
def test_open_browser_help_modal(base_url, selenium):
    slug = ""
    page = FirefoxAllPage(selenium, base_url, slug=slug).open()
    modal = page.open_help_modal("icon-browser-help")
    assert modal.is_displayed


@pytest.mark.skipif(
    settings.ENABLE_FIREFOX_COM_REDIRECTS is True,
    reason="Related view is now unreachable and [TODO] should be removed",
)
@pytest.mark.smoke
@pytest.mark.nondestructive
def test_open_installer_help_modal(base_url, selenium):
    slug = "desktop-release/"
    page = FirefoxAllPage(selenium, base_url, slug=slug).open()
    modal = page.open_help_modal("icon-installer-help")
    assert modal.is_displayed
