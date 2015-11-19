# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from selenium.common.exceptions import TimeoutException

from pages.contribute.contribute import ContributePage


@pytest.mark.sanity
@pytest.mark.nondestructive
def test_play_video(base_url, selenium):
    page = ContributePage(base_url, selenium).open()
    video = page.play_video()
    assert video.is_displayed
    video.close()


@pytest.mark.nondestructive
def test_next_event_is_displayed(base_url, selenium):
    page = ContributePage(base_url, selenium).open()
    assert page.next_event_is_displayed


@pytest.mark.sanity
@pytest.mark.nondestructive
def test_newsletter_default_values(base_url, selenium):
    page = ContributePage(base_url, selenium).open()
    page.newsletter.expand_form()
    assert '' == page.newsletter.email
    assert 'United States' == page.newsletter.country
    assert page.newsletter.html_format_selected
    assert not page.newsletter.text_format_selected
    assert not page.newsletter.privacy_policy_accepted
    assert page.newsletter.is_privacy_policy_link_displayed


def test_newsletter_successful_sign_up(base_url, selenium):
    page = ContributePage(base_url, selenium).open()
    page.newsletter.expand_form()
    page.newsletter.type_email('noreply@mozilla.com')
    page.newsletter.select_country('United Kingdom')
    page.newsletter.select_text_format()
    page.newsletter.accept_privacy_policy()
    page.newsletter.click_sign_me_up()
    assert page.newsletter.sign_up_successful


@pytest.mark.nondestructive
def test_newsletter_sign_up_fails_when_missing_required_fields(base_url, selenium):
    page = ContributePage(base_url, selenium).open()
    page.newsletter.expand_form()
    with pytest.raises(TimeoutException):
        page.newsletter.click_sign_me_up()
