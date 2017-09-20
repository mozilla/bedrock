# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from selenium.common.exceptions import TimeoutException
from pages.firefox.ios_testflight import iOSTestFlightPage


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_signup_default_values(base_url, selenium):
    page = iOSTestFlightPage(selenium, base_url).open()
    assert '' == page.email
    assert not page.privacy_policy_accepted
    assert not page.terms_accepted
    assert page.is_privacy_policy_link_displayed
    assert page.is_terms_link_displayed


@pytest.mark.nondestructive
def test_successful_sign_up(base_url, selenium):
    page = iOSTestFlightPage(selenium, base_url).open()
    page.type_email('success@example.com')
    page.accept_privacy_policy()
    page.accept_terms()
    page.click_sign_me_up()
    assert page.sign_up_successful


@pytest.mark.nondestructive
def test_sign_up_fails_when_missing_required_fields(base_url, selenium):
    page = iOSTestFlightPage(selenium, base_url).open()
    with pytest.raises(TimeoutException):
        page.click_sign_me_up()
