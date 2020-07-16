# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from selenium.common.exceptions import TimeoutException

from pages.home import HomePage
from pages.about import AboutPage
from pages.contribute.contribute import ContributePage
from pages.mission import MissionPage
from pages.firefox.whatsnew.whatsnew_developer_70 import FirefoxWhatsNewDeveloper70Page
from pages.newsletter.developer import DeveloperNewsletterPage
from pages.newsletter.firefox import FirefoxNewsletterPage
from pages.newsletter.mozilla import MozillaNewsletterPage


@pytest.mark.nondestructive
@pytest.mark.parametrize('page_class', [
    HomePage,
    AboutPage,
    MissionPage,
    pytest.mark.skip_if_not_firefox(FirefoxWhatsNewDeveloper70Page),
    DeveloperNewsletterPage,
    FirefoxNewsletterPage,
    MozillaNewsletterPage])
def test_newsletter_default_values(page_class, base_url, selenium):
    page = page_class(selenium, base_url).open()
    page.newsletter.expand_form()
    assert '' == page.newsletter.email
    assert 'United States' == page.newsletter.country
    assert not page.newsletter.privacy_policy_accepted
    assert page.newsletter.is_privacy_policy_link_displayed


@pytest.mark.nondestructive
@pytest.mark.parametrize('page_class', [
    HomePage,
    AboutPage,
    MissionPage,
    ContributePage,
    pytest.mark.skip_if_not_firefox(FirefoxWhatsNewDeveloper70Page),
    DeveloperNewsletterPage,
    FirefoxNewsletterPage,
    MozillaNewsletterPage])
def test_newsletter_successful_sign_up(page_class, base_url, selenium):
    page = page_class(selenium, base_url).open()
    page.newsletter.expand_form()
    page.newsletter.type_email('success@example.com')
    page.newsletter.select_country('United Kingdom')
    page.newsletter.select_text_format()
    page.newsletter.accept_privacy_policy()
    page.newsletter.click_sign_me_up()
    assert page.newsletter.sign_up_successful


@pytest.mark.nondestructive
@pytest.mark.parametrize('page_class', [
    HomePage,
    AboutPage,
    MissionPage,
    ContributePage,
    pytest.mark.skip_if_not_firefox(FirefoxWhatsNewDeveloper70Page),
    DeveloperNewsletterPage,
    FirefoxNewsletterPage,
    MozillaNewsletterPage])
def test_newsletter_sign_up_fails_when_missing_required_fields(page_class, base_url, selenium):
    page = page_class(selenium, base_url).open()
    page.newsletter.expand_form()
    with pytest.raises(TimeoutException):
        page.newsletter.click_sign_me_up()
