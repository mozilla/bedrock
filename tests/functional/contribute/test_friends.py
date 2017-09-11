# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from selenium.common.exceptions import TimeoutException
from pages.contribute.friends import ContributeFriendsPage


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_signup_default_values(base_url, selenium):
    page = ContributeFriendsPage(selenium, base_url).open()
    assert '' == page.email
    assert 'United States' == page.country
    assert not page.privacy_policy_accepted
    assert page.is_privacy_policy_link_displayed


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_click_fx_and_you(base_url, selenium):
    page = ContributeFriendsPage(selenium, base_url).open()
    assert page.newsletters == 'firefox-friends'
    page.accept_fx_and_you()
    assert page.newsletters == 'firefox-friends,mozilla-and-you'


@pytest.mark.nondestructive
def test_successful_sign_up(base_url, selenium):
    page = ContributeFriendsPage(selenium, base_url).open()
    page.type_email('success@example.com')
    page.select_country('Germany')
    page.accept_privacy_policy()
    page.click_sign_me_up()
    assert page.sign_up_successful


@pytest.mark.nondestructive
def test_sign_up_fails_when_missing_required_fields(base_url, selenium):
    page = ContributeFriendsPage(selenium, base_url).open()
    with pytest.raises(TimeoutException):
        page.click_sign_me_up()
