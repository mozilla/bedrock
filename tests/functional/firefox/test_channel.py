# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.channel import ChannelPage


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_download_carousel_buttons(base_url, selenium):
    page = ChannelPage(base_url, selenium, hash='').open()
    assert page.desktop_beta_download_button.is_displayed
    assert page.android_beta_download_button.is_displayed
    page.click_next()
    assert page.desktop_release_download_button.is_displayed
    assert page.android_release_download_button.is_displayed
    page.click_next()
    assert page.desktop_developer_download_button.is_displayed
    assert page.android_aurora_download_button.is_displayed
    page.click_previous()
    assert page.desktop_release_download_button.is_displayed
    assert page.android_release_download_button.is_displayed


@pytest.mark.nondestructive
def test_download_beta_url_hash(base_url, selenium):
    page = ChannelPage(base_url, selenium, hash='#beta').open()
    assert page.desktop_beta_download_button.is_displayed
    assert page.android_beta_download_button.is_displayed


@pytest.mark.nondestructive
def test_download_release_url_hash(base_url, selenium):
    page = ChannelPage(base_url, selenium, hash='#firefox').open()
    assert page.desktop_release_download_button.is_displayed
    assert page.android_release_download_button.is_displayed


@pytest.mark.nondestructive
def test_download_developer_url_hash(base_url, selenium):
    page = ChannelPage(base_url, selenium, hash='#developer').open()
    assert page.desktop_developer_download_button.is_displayed
    assert page.android_aurora_download_button.is_displayed
