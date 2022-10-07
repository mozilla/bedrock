# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.ios_testflight import iOSTestFlightPage


@pytest.mark.nondestructive
def test_signup_default_values(base_url, selenium):
    page = iOSTestFlightPage(selenium, base_url).open()
    page.expand_form()
    assert "" == page.email
    assert page.html_format_selected
    assert not page.text_format_selected
    assert not page.privacy_policy_accepted
    assert not page.terms_accepted
    assert page.is_privacy_policy_link_displayed
    assert page.is_terms_link_displayed


@pytest.mark.nondestructive
def test_sign_up_success(base_url, selenium):
    page = iOSTestFlightPage(selenium, base_url).open()
    assert not page.sign_up_successful
    page.expand_form()
    page.type_email("success@example.com")
    page.select_text_format()
    page.accept_privacy_policy()
    page.accept_terms()
    page.click_sign_me_up()
    assert page.sign_up_successful


@pytest.mark.nondestructive
def test_sign_up_failure(base_url, selenium):
    page = iOSTestFlightPage(selenium, base_url).open()
    assert not page.is_form_error_displayed
    page.expand_form()
    page.type_email("invalid@email")
    page.select_text_format()
    page.accept_privacy_policy()
    page.accept_terms()
    page.click_sign_me_up(expected_result="error")
    assert page.is_form_error_displayed
