# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.sync import FirefoxSyncPage


@pytest.mark.skip_if_firefox
@pytest.mark.nondestructive
def test_download_button_is_displayed(base_url, selenium):
    page = FirefoxSyncPage(base_url, selenium).open()
    assert page.download_button.is_displayed


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_app_store_buttons_displayed(base_url, selenium):
    page = FirefoxSyncPage(base_url, selenium).open()
    assert page.is_play_store_button_displayed
    assert page.is_app_store_button_displayed


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_newsletter_default_values(base_url, selenium):
    page = FirefoxSyncPage(base_url, selenium).open()
    page.newsletter.expand_form()
    assert '' == page.newsletter.email
    assert 'United States' == page.newsletter.country
    assert not page.newsletter.privacy_policy_accepted
    assert page.newsletter.is_privacy_policy_link_displayed
