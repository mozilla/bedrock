# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.developer import DeveloperPage


@pytest.mark.sanity
@pytest.mark.nondestructive
def test_download_buttons_are_displayed(base_url, selenium):
    page = DeveloperPage(base_url, selenium).open()
    assert page.is_primary_download_button_displayed
    assert page.is_secondary_download_button_displayed


@pytest.mark.skipif(reason='https://bugzilla.mozilla.org/show_bug.cgi?id=1219251')
@pytest.mark.sanity
@pytest.mark.nondestructive
def test_play_video(base_url, selenium):
    page = DeveloperPage(base_url, selenium).open()
    video = page.developer_videos[0].play()
    assert video.is_displayed
    video.close()
