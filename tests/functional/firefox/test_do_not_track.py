# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.do_not_track import DoNotTrackPage


@pytest.mark.sanity
@pytest.mark.nondestructive
def test_family_navigation(base_url, selenium):
    page = DoNotTrackPage(base_url, selenium).open()
    page.family_navigation.open_menu()
    assert page.family_navigation.is_menu_displayed


@pytest.mark.sanity
@pytest.mark.nondestructive
def test_dnt_status(base_url, selenium):
    page = DoNotTrackPage(base_url, selenium).open()
    assert page.is_do_not_track_status_displayed


@pytest.mark.sanity
@pytest.mark.nondestructive
def test_open_and_close_faq_panel(base_url, selenium):
    page = DoNotTrackPage(base_url, selenium).open()
    question = page.frequently_asked_questions[0]
    question.show_answer()
    assert question.is_answer_displayed
    question.hide_answer()
    assert not question.is_answer_displayed
