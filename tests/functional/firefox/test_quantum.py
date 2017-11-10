# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.quantum import FirefoxQuantumPage


@pytest.mark.skipif(reason='https://bugzilla.mozilla.org/show_bug.cgi?id=1415599')
@pytest.mark.nondestructive
def test_modal_successful_sign_up(base_url, selenium):
    page = FirefoxQuantumPage(selenium, base_url).open()
    modal = page.open_sign_up_modal()
    assert modal.is_displayed
    page.newsletter.expand_form()
    page.newsletter.type_email('success@example.com')
    page.newsletter.select_country('United Kingdom')
    page.newsletter.select_text_format()
    page.newsletter.accept_privacy_policy()
    page.newsletter.click_sign_me_up()
    assert page.newsletter.sign_up_successful
    modal.close()


@pytest.mark.skipif(reason='https://bugzilla.mozilla.org/show_bug.cgi?id=1415599')
@pytest.mark.nondestructive
def test_video_carousel(base_url, selenium):
    page = FirefoxQuantumPage(selenium, base_url).open()
    carousel = page.video_carousel
    assert carousel.is_bookmarking_video_displayed
    carousel.click_next()
    assert carousel.is_new_tab_video_displayed
    carousel.click_next()
    assert carousel.is_screenshots_video_displayed
    carousel.click_previous()
    assert carousel.is_new_tab_video_displayed
