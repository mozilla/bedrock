# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

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
