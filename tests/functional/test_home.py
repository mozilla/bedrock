# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from selenium.common.exceptions import TimeoutException

from ..pages.home import HomePage


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


@pytest.mark.nondestructive
def test_download_button_is_displayed(base_url, selenium):
    page = HomePage(base_url, selenium).open()
    assert page.is_download_button_displayed


@pytest.mark.nondestructive
def test_upcoming_events_are_displayed(base_url, selenium):
    page = HomePage(base_url, selenium).open()
    events = page.upcoming_events
    assert events.is_next_event_displayed
    assert events.is_events_list_displayed


@pytest.mark.nondestructive
def test_mozilla_newsletter_default_values(base_url, selenium):
    page = HomePage(base_url, selenium).open()
    page.mozilla_newsletter.expand_form()
    assert '' == page.mozilla_newsletter.email
    assert 'United States' == page.mozilla_newsletter.country
    assert not page.mozilla_newsletter.privacy_policy_accepted


def test_mozilla_newsletter_successful_sign_up(base_url, selenium):
    page = HomePage(base_url, selenium).open()
    newsletter = page.mozilla_newsletter
    newsletter.expand_form()
    newsletter.type_email('noreply@mozilla.com')
    newsletter.select_country('United Kingdom')
    newsletter.accept_privacy_policy()
    newsletter.click_sign_me_up()
    assert newsletter.sign_up_successful


@pytest.mark.nondestructive
def test_mozilla_newsletter_sign_up_fails_when_missing_required_fields(base_url, selenium):
    page = HomePage(base_url, selenium).open()
    page.mozilla_newsletter.expand_form()
    with pytest.raises(TimeoutException):
        page.mozilla_newsletter.click_sign_me_up()
