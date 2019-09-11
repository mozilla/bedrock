# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from selenium.common.exceptions import TimeoutException

from pages.home import HomePage
from pages.about import AboutPage
from pages.contribute.contribute import ContributePage
from pages.mission import MissionPage
from pages.firefox.features.landing import FeaturesLandingPage
from pages.plugincheck import PluginCheckPage


@pytest.mark.nondestructive
@pytest.mark.parametrize('page_class', [HomePage, AboutPage, MissionPage])
def test_newsletter_default_values(page_class, base_url, selenium):
    page = page_class(selenium, base_url).open()
    page.newsletter.expand_form()
    assert '' == page.newsletter.email
    assert 'United States' == page.newsletter.country
    assert not page.newsletter.privacy_policy_accepted
    assert page.newsletter.is_privacy_policy_link_displayed


@pytest.mark.nondestructive
@pytest.mark.parametrize('page_class', [HomePage, AboutPage, MissionPage])
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
@pytest.mark.parametrize('page_class', [HomePage, AboutPage, MissionPage])
def test_newsletter_sign_up_fails_when_missing_required_fields(page_class, base_url, selenium):
    page = page_class(selenium, base_url).open()
    page.newsletter.expand_form()
    with pytest.raises(TimeoutException):
        page.newsletter.click_sign_me_up()


@pytest.mark.nondestructive
@pytest.mark.parametrize(('page_class', 'url_kwargs'), [
    (ContributePage, None),
    (FeaturesLandingPage, None),
    (PluginCheckPage, None)])
def test_legacy_newsletter_default_values(page_class, url_kwargs, base_url, selenium):
    url_kwargs = url_kwargs or {}
    page = page_class(selenium, base_url, **url_kwargs).open()
    page.legacy_newsletter.expand_form()
    assert '' == page.legacy_newsletter.email
    assert 'United States' == page.legacy_newsletter.country
    assert not page.legacy_newsletter.privacy_policy_accepted
    assert page.legacy_newsletter.is_privacy_policy_link_displayed


@pytest.mark.nondestructive
@pytest.mark.parametrize('page_class', [ContributePage])
def test_legacy_newsletter_successful_sign_up(page_class, base_url, selenium):
    page = page_class(selenium, base_url).open()
    page.legacy_newsletter.expand_form()
    page.legacy_newsletter.type_email('success@example.com')
    page.legacy_newsletter.select_country('United Kingdom')
    page.legacy_newsletter.select_text_format()
    page.legacy_newsletter.accept_privacy_policy()
    page.legacy_newsletter.click_sign_me_up()
    assert page.legacy_newsletter.sign_up_successful


@pytest.mark.nondestructive
@pytest.mark.parametrize('page_class', [ContributePage])
def test_legacy_newsletter_sign_up_fails_when_missing_required_fields(page_class, base_url, selenium):
    page = page_class(selenium, base_url).open()
    page.legacy_newsletter.expand_form()
    with pytest.raises(TimeoutException):
        page.legacy_newsletter.click_sign_me_up()
