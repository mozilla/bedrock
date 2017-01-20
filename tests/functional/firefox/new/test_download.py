# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.new.download import DownloadPage


@pytest.mark.smoke
@pytest.mark.sanity
@pytest.mark.nondestructive
def test_download_button_displayed(base_url, selenium):
    page = DownloadPage(selenium, base_url).open()
    assert page.download_button.is_displayed


@pytest.mark.skip_if_internet_explorer(reason='https://github.com/SeleniumHQ/selenium/issues/448')
@pytest.mark.smoke
@pytest.mark.sanity
@pytest.mark.nondestructive
def test_click_download_button(base_url, selenium):
    page = DownloadPage(selenium, base_url).open()
    thank_you_page = page.download_firefox()
    assert thank_you_page.seed_url in selenium.current_url


@pytest.mark.nondestructive
def test_other_platforms_modal(base_url, selenium):
    page = DownloadPage(selenium, base_url).open()
    modal = page.open_other_platforms_modal()
    assert modal.is_displayed
    modal.close()
