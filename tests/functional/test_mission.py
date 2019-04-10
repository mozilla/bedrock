# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.mission import MissionPage


@pytest.mark.nondestructive
def test_play_video(base_url, selenium):
    page = MissionPage(selenium, base_url).open()
    page.play_video()
    assert not page.is_video_overlay_displayed
    assert page.is_video_displayed
