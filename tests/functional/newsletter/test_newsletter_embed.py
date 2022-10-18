# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.about import AboutPage
from pages.contribute.contribute import ContributePage
from pages.firefox.whatsnew.whatsnew_developer_70 import FirefoxWhatsNewDeveloper70Page
from pages.home import HomePage
from pages.mission import MissionPage
from pages.newsletter.developer import DeveloperNewsletterPage
from pages.newsletter.family import FamilyNewsletterPage
from pages.newsletter.firefox import FirefoxNewsletterPage
from pages.newsletter.index import NewsletterPage
from pages.newsletter.knowledge_is_power import KnowledgeIsPowerNewsletterPage
from pages.newsletter.mozilla import MozillaNewsletterPage


@pytest.mark.smoke
@pytest.mark.nondestructive
@pytest.mark.parametrize(
    "page_class",
    [
        HomePage,
        AboutPage,
        MissionPage,
        pytest.mark.skip_if_not_firefox(FirefoxWhatsNewDeveloper70Page),
        NewsletterPage,
        DeveloperNewsletterPage,
        FirefoxNewsletterPage,
        MozillaNewsletterPage,
        KnowledgeIsPowerNewsletterPage,
        FamilyNewsletterPage,
    ],
)
def test_newsletter_default_values(page_class, base_url, selenium):
    page = page_class(selenium, base_url).open()
    page.newsletter.expand_form()
    assert "" == page.newsletter.email
    assert "United States" == page.newsletter.country
    assert not page.newsletter.privacy_policy_accepted
    assert page.newsletter.is_privacy_policy_link_displayed


@pytest.mark.smoke
@pytest.mark.nondestructive
@pytest.mark.parametrize(
    "page_class",
    [
        HomePage,
        AboutPage,
        MissionPage,
        ContributePage,
        pytest.mark.skip_if_not_firefox(FirefoxWhatsNewDeveloper70Page),
        NewsletterPage,
        DeveloperNewsletterPage,
        FirefoxNewsletterPage,
        MozillaNewsletterPage,
        KnowledgeIsPowerNewsletterPage,
        FamilyNewsletterPage,
    ],
)
def test_newsletter_sign_up_success(page_class, base_url, selenium):
    page = page_class(selenium, base_url).open()
    assert not page.newsletter.sign_up_successful
    page.newsletter.expand_form()
    page.newsletter.type_email("success@example.com")
    page.newsletter.select_country("United Kingdom")
    page.newsletter.select_text_format()
    page.newsletter.accept_privacy_policy()
    page.newsletter.click_sign_me_up()
    assert page.newsletter.sign_up_successful


@pytest.mark.smoke
@pytest.mark.nondestructive
@pytest.mark.parametrize(
    "page_class",
    [
        HomePage,
        AboutPage,
        MissionPage,
        ContributePage,
        pytest.mark.skip_if_not_firefox(FirefoxWhatsNewDeveloper70Page),
        NewsletterPage,
        DeveloperNewsletterPage,
        FirefoxNewsletterPage,
        MozillaNewsletterPage,
        KnowledgeIsPowerNewsletterPage,
        FamilyNewsletterPage,
    ],
)
def test_newsletter_sign_up_failure(page_class, base_url, selenium):
    page = page_class(selenium, base_url).open()
    assert not page.newsletter.is_form_error_displayed
    page.newsletter.expand_form()
    page.newsletter.type_email("failure@example.com")
    page.newsletter.select_country("United Kingdom")
    page.newsletter.select_text_format()
    page.newsletter.accept_privacy_policy()
    page.newsletter.click_sign_me_up(expected_result="error")
    assert page.newsletter.is_form_error_displayed
