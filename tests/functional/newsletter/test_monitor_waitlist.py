# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.newsletter.monitor_waitlist import MonitorWaitlistNewsletterPage


@pytest.mark.nondestructive
def test_monitor_waitlist_success(base_url, selenium):
    page = MonitorWaitlistNewsletterPage(selenium, base_url, params="?geo=us").open()
    assert not page.newsletter.sign_up_successful
    page.newsletter.expand_form()
    page.newsletter.type_email("success@example.com")
    page.newsletter.select_text_format()
    page.newsletter.accept_privacy_policy()
    page.newsletter.click_sign_me_up()
    assert page.newsletter.sign_up_successful


@pytest.mark.nondestructive
def test_monitor_waitlist_failure(base_url, selenium):
    page = MonitorWaitlistNewsletterPage(selenium, base_url, params="?geo=us").open()
    assert not page.newsletter.is_form_error_displayed
    page.newsletter.expand_form()
    page.newsletter.type_email("failure@example.com")
    page.newsletter.select_text_format()
    page.newsletter.accept_privacy_policy()
    page.newsletter.click_sign_me_up(expected_result="error")
    assert page.newsletter.is_form_error_displayed


@pytest.mark.nondestructive
def test_monitor_waitlist_unavailable_country(base_url, selenium):
    page = MonitorWaitlistNewsletterPage(selenium, base_url, params="?geo=de").open()
    assert page.is_unavailable_country_message_displayed
