# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.new import FirefoxNewPage, FirefoxNewThankYouPage


# We don't currently show the download button for up-to-date Firefox users.
# TODO explore how could we run this test using a known out-of-date Firefox?

@pytest.mark.skip_if_firefox
@pytest.mark.smoke
@pytest.mark.sanity
@pytest.mark.nondestructive
def test_download_button_displayed(base_url, selenium):
    page = FirefoxNewPage(base_url, selenium).open()
    assert page.download_button.is_displayed


# skip tests that trigger download bar in IE due to https://github.com/SeleniumHQ/selenium/issues/448
@pytest.mark.skip_if_firefox
@pytest.mark.skip_if_internet_explorer
@pytest.mark.smoke
@pytest.mark.sanity
@pytest.mark.nondestructive
def test_click_download_button(base_url, selenium):
    page = FirefoxNewPage(base_url, selenium).open()
    page.download_firefox()
    assert page.is_thank_you_message_displayed


# skip tests that trigger download bar in IE due to https://github.com/SeleniumHQ/selenium/issues/448
@pytest.mark.skip_if_internet_explorer
@pytest.mark.smoke
@pytest.mark.sanity
@pytest.mark.nondestructive
def test_directly_load_thank_you(base_url, selenium):
    page = FirefoxNewThankYouPage(base_url, selenium).open()
    assert page.is_thank_you_message_displayed
