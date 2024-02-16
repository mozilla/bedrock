# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.newsletter.family import NewsletterFamilyPage


@pytest.mark.nondestructive
def test_newsletter_family_success(base_url, selenium):
    page = NewsletterFamilyPage(selenium, base_url).open()
    assert not page.newsletter.sign_up_successful
    page.newsletter.expand_form()
    page.newsletter.type_email("success@example.com")
    page.newsletter.select_text_format()
    page.newsletter.accept_privacy_policy()
    page.newsletter.click_sign_me_up()
    assert page.newsletter.sign_up_successful


@pytest.mark.nondestructive
def test_newsletter_family_failure(base_url, selenium):
    page = NewsletterFamilyPage(selenium, base_url).open()
    assert not page.newsletter.is_form_error_displayed
    page.newsletter.expand_form()
    page.newsletter.type_email("failure@example.com")
    page.newsletter.select_text_format()
    page.newsletter.accept_privacy_policy()
    page.newsletter.click_sign_me_up(expected_result="error")
    assert page.newsletter.is_form_error_displayed
