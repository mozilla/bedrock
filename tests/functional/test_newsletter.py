# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from selenium.common.exceptions import TimeoutException

from pages.newsletter import NewsletterPage


@pytest.mark.sanity
@pytest.mark.nondestructive
def test_default_values(base_url, selenium):
    page = NewsletterPage(base_url, selenium).open()
    assert '' == page.email
    assert 'United States' == page.country
    assert 'English' == page.language
    assert page.html_format_selected
    assert not page.text_format_selected
    assert not page.privacy_policy_accepted
    assert page.is_privacy_policy_link_displayed


@pytest.mark.flaky(reruns=1)
def test_successful_sign_up(base_url, selenium):
    page = NewsletterPage(base_url, selenium).open()
    page.type_email('noreply@mozilla.com')
    page.select_country('United Kingdom')
    page.select_language('Polski')
    page.select_text_format()
    page.accept_privacy_policy()
    page.click_sign_me_up()
    assert page.sign_up_successful


@pytest.mark.nondestructive
def test_sign_up_fails_when_missing_required_fields(base_url, selenium):
    page = NewsletterPage(base_url, selenium).open()
    with pytest.raises(TimeoutException):
        page.click_sign_me_up()
