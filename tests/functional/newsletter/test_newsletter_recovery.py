# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.newsletter.recovery import NewsletterRecoveryPage


@pytest.mark.nondestructive
def test_newsletter_recovery_success(base_url, selenium):
    page = NewsletterRecoveryPage(selenium, base_url).open()
    page.type_email("success@example.com")
    page.click_submit()
    assert page.is_success_message_displayed


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_newsletter_recovery_failure(base_url, selenium):
    page = NewsletterRecoveryPage(selenium, base_url).open()
    page.type_email("failure@example.com")
    page.click_submit(expected_result="error")
    assert page.is_error_message_displayed
