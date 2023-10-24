# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.products.monitor.waitlist import MonitorWaitlistPage


@pytest.mark.nondestructive
@pytest.mark.parametrize("slug", [("plus"), ("scan")])
def test_not_available_in_country(slug, base_url, selenium):
    page = MonitorWaitlistPage(selenium, base_url, slug=slug, params="?geo=GB").open()
    assert not page.is_newsletter_form_displayed
    assert page.is_service_not_available_message_displayed


@pytest.mark.nondestructive
@pytest.mark.parametrize("slug", [("plus"), ("scan")])
def test_signup_success(slug, base_url, selenium):
    page = MonitorWaitlistPage(selenium, base_url, slug=slug, params="?geo=US").open()
    page.expand_form()
    page.type_email("success@example.com")
    page.newsletter.accept_privacy_policy()
    page.click_sign_up_now()
    assert page.is_form_success_displayed


@pytest.mark.nondestructive
@pytest.mark.parametrize("slug", [("plus"), ("scan")])
def test_signup_failure(slug, base_url, selenium):
    page = MonitorWaitlistPage(selenium, base_url, slug=slug, params="?geo=US").open()
    page.expand_form()
    page.type_email("failure@example.com")
    page.newsletter.accept_privacy_policy()
    page.click_sign_up_now(expected_result="error")
    assert page.is_form_error_displayed
