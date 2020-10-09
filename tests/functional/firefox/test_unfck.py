# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.unfck import FirefoxUnfckPage


@pytest.mark.skip_if_firefox(reason='Download button is displayed only to non-Firefox users')
@pytest.mark.nondestructive
@pytest.mark.parametrize('locale', [
    ('en-US'),
    ('de'),
    ('fr')])
def test_download_button_displayed(locale, base_url, selenium):
    page = FirefoxUnfckPage(selenium, base_url, locale=locale).open()
    assert page.download_button.is_displayed


@pytest.mark.skip_if_not_firefox(reason='App Store badges are displayed only to Firefox users')
def test_app_store_buttons_displayed(base_url, selenium):
    page = FirefoxUnfckPage(selenium, base_url).open()
    assert page.is_play_store_button_displayed
    assert page.is_app_store_button_displayed


@pytest.mark.skip_if_not_firefox(reason='Facebook Container button is displayed only to Firefox users')
@pytest.mark.parametrize('locale', [
    ('de'),
    ('fr')])
def test_facebook_container_button_displayed(locale, base_url, selenium):
    page = FirefoxUnfckPage(selenium, base_url, locale=locale).open()
    assert page.is_facebook_container_button_displayed
