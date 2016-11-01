# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from selenium.common.exceptions import TimeoutException

from pages.newsletter.developer import DeveloperNewsletterPage
from pages.newsletter.firefox import FirefoxNewsletterPage
from pages.newsletter.mozilla import MozillaNewsletterPage


@pytest.mark.smoke
@pytest.mark.nondestructive
@pytest.mark.parametrize('page_class', [FirefoxNewsletterPage, MozillaNewsletterPage])
def test_default_values(page_class, base_url, selenium):
    page = page_class(selenium, base_url).open()
    assert '' == page.email
    assert 'United States' == page.country
    assert 'English' == page.language
    assert page.html_format_selected
    assert not page.text_format_selected
    assert not page.privacy_policy_accepted
    assert page.is_privacy_policy_link_displayed


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_default_values_developer_newsletter(base_url, selenium):
    page = DeveloperNewsletterPage(selenium, base_url).open()
    assert '' == page.email
    assert 'United States' == page.country
    assert page.html_format_selected
    assert not page.text_format_selected
    assert not page.privacy_policy_accepted
    assert page.is_privacy_policy_link_displayed


@pytest.mark.nondestructive
@pytest.mark.parametrize('page_class', [FirefoxNewsletterPage, MozillaNewsletterPage])
def test_successful_sign_up(page_class, base_url, selenium):
    page = page_class(selenium, base_url).open()
    page.type_email('success@example.com')
    page.select_country('United Kingdom')
    page.select_language('Deutsch')
    page.select_text_format()
    page.accept_privacy_policy()
    page.click_sign_me_up()
    assert page.sign_up_successful


@pytest.mark.nondestructive
def test_successful_sign_up_developer_newsletter(base_url, selenium):
    page = DeveloperNewsletterPage(selenium, base_url).open()
    page.type_email('success@example.com')
    page.select_country('United Kingdom')
    page.select_text_format()
    page.accept_privacy_policy()
    page.click_sign_me_up()
    assert page.sign_up_successful


@pytest.mark.nondestructive
@pytest.mark.parametrize('page_class', [DeveloperNewsletterPage, FirefoxNewsletterPage, MozillaNewsletterPage])
def test_sign_up_fails_when_missing_required_fields(page_class, base_url, selenium):
    page = page_class(selenium, base_url).open()
    with pytest.raises(TimeoutException):
        page.click_sign_me_up()
