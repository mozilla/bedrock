# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from selenium.common.exceptions import TimeoutException

from pages.home import HomePage


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_promo_grid_is_displayed(base_url, selenium):
    page = HomePage(base_url, selenium).open()
    assert page.is_promo_grid_displayed


@pytest.mark.nondestructive
def test_promos_are_present(base_url, selenium):
    page = HomePage(base_url, selenium).open()
    assert page.number_of_promos_present == 16


@pytest.mark.nondestructive
def test_tweet_is_present(base_url, selenium):
    page = HomePage(base_url, selenium).open()
    assert page.is_tweet_promo_present


@pytest.mark.nondestructive
def test_tweet_is_not_present(base_url, selenium):
    page = HomePage(base_url, selenium, 'de').open()
    assert not page.is_tweet_promo_present


@pytest.mark.sanity
@pytest.mark.smoke
@pytest.mark.nondestructive
def test_download_button_is_displayed(base_url, selenium):
    page = HomePage(base_url, selenium).open()
    assert page.download_button.is_displayed


@pytest.mark.nondestructive
def test_upcoming_events_are_displayed(base_url, selenium):
    page = HomePage(base_url, selenium).open()
    events = page.upcoming_events
    assert events.is_next_event_displayed
    assert events.is_events_list_displayed


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_newsletter_default_values(base_url, selenium):
    page = HomePage(base_url, selenium).open()
    page.newsletter.expand_form()
    assert '' == page.newsletter.email
    assert 'United States' == page.newsletter.country
    assert not page.newsletter.privacy_policy_accepted
    assert page.newsletter.is_privacy_policy_link_displayed


@pytest.mark.flaky(reruns=1, reason='https://bugzilla.mozilla.org/show_bug.cgi?id=1218451')
def test_newsletter_successful_sign_up(base_url, selenium):
    page = HomePage(base_url, selenium).open()
    newsletter = page.newsletter
    newsletter.expand_form()
    newsletter.type_email('noreply@mozilla.com')
    newsletter.select_country('United Kingdom')
    newsletter.select_text_format()
    newsletter.accept_privacy_policy()
    newsletter.click_sign_me_up()
    assert newsletter.sign_up_successful


@pytest.mark.nondestructive
def test_newsletter_sign_up_fails_when_missing_required_fields(base_url, selenium):
    page = HomePage(base_url, selenium).open()
    page.newsletter.expand_form()
    with pytest.raises(TimeoutException):
        page.newsletter.click_sign_me_up()
