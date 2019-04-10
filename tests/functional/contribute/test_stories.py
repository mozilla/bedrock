# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.contribute.stories import ContributeStoriesPage


@pytest.mark.nondestructive
def test_show_hide_story(base_url, selenium):
    page = ContributeStoriesPage(selenium, base_url).open()
    page.show_story()
    assert page.is_story_displayed
    page.hide_story()
    assert not page.is_story_displayed


@pytest.mark.nondestructive
def test_next_event_is_displayed(base_url, selenium):
    page = ContributeStoriesPage(selenium, base_url).open()
    assert page.next_event_is_displayed
