# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.contribute.contribute import ContributePage


@pytest.mark.nondestructive
def test_play_video(base_url, selenium):
    page = ContributePage(selenium, base_url, locale='es-ES').open()
    video = page.play_video()
    assert video.is_displayed
    video.close()
