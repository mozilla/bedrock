# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.hello import HelloPage


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_play_video(base_url, selenium):
    page = HelloPage(base_url, selenium).open()
    video = page.play_video()
    assert video.is_displayed
    video.close()


@pytest.mark.skip_if_not_firefox
@pytest.mark.smoke
@pytest.mark.nondestructive
def test_try_hello_button_is_displayed(base_url, selenium):
    page = HelloPage(base_url, selenium).open()
    assert page.is_try_hello_button_displayed
    assert not page.download_button.is_displayed


@pytest.mark.skip_if_firefox
@pytest.mark.smoke
@pytest.mark.nondestructive
def test_download_button_is_displayed(base_url, selenium):
    page = HelloPage(base_url, selenium).open()
    assert page.download_button.is_displayed
    assert not page.is_try_hello_button_displayed
