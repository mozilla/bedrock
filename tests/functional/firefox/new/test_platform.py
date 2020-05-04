# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.new.platform import PlatformDownloadPage


@pytest.mark.sanity
@pytest.mark.nondestructive
@pytest.mark.parametrize('slug', ['windows', 'mac', 'linux'])
def test_download_button_displayed(slug, base_url, selenium):
    page = PlatformDownloadPage(selenium, base_url, slug=slug).open()
    assert page.download_button.is_displayed


# Firefox and Internet Explorer don't cope well with file prompts whilst using Selenium.
@pytest.mark.skip_if_firefox(reason='http://saucelabs.com/jobs/5a8a62a7620f489d92d6193fa67cf66b')
@pytest.mark.skip_if_internet_explorer(reason='https://github.com/SeleniumHQ/selenium/issues/448')
@pytest.mark.nondestructive
@pytest.mark.parametrize('slug', ['windows', 'mac', 'linux'])
def test_click_download_button(slug, base_url, selenium):
    page = PlatformDownloadPage(selenium, base_url, slug=slug).open()
    thank_you_page = page.download_firefox()
    assert thank_you_page.seed_url in selenium.current_url


@pytest.mark.nondestructive
@pytest.mark.parametrize('slug', ['windows', 'mac', 'linux'])
def test_other_platforms_modal(slug, base_url, selenium):
    page = PlatformDownloadPage(selenium, base_url, slug=slug).open()
    modal = page.open_other_platforms_modal()
    assert modal.is_displayed
    modal.close()
