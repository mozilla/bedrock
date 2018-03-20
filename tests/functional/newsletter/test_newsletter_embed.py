# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from selenium.common.exceptions import TimeoutException

from pages.home import HomePage
from pages.about import AboutPage
from pages.contribute.contribute import ContributePage
from pages.contribute.task.twitter import TwitterTaskPage
from pages.contribute.task.mobile import MobileTaskPage
from pages.contribute.task.encryption import EncryptionTaskPage
from pages.contribute.task.joy_of_coding import JoyOfCodingTaskPage
from pages.contribute.task.dev_tools_challenger import DevToolsChallengerTaskPage
from pages.contribute.task.stumbler import StumblerTaskPage
from pages.mission import MissionPage
from pages.firefox.all import FirefoxAllPage
from pages.firefox.features.feature import FeaturePage
from pages.plugincheck import PluginCheckPage
from pages.smarton.landing import SmartOnLandingPage
from pages.smarton.base import SmartOnBasePage


@pytest.mark.nondestructive
@pytest.mark.parametrize(('page_class', 'url_kwargs'), [
    pytest.mark.skipif((HomePage, None), reason='https://bugzilla.mozilla.org/show_bug.cgi?id=1443566'),
    (AboutPage, None),
    pytest.mark.smoke((ContributePage, None)),
    (TwitterTaskPage, None),
    (MobileTaskPage, None),
    (EncryptionTaskPage, None),
    (JoyOfCodingTaskPage, None),
    (DevToolsChallengerTaskPage, None),
    (StumblerTaskPage, None),
    (MissionPage, None),
    (FirefoxAllPage, None),
    (FeaturePage, {'slug': 'sync'}),
    (PluginCheckPage, None),
    (SmartOnLandingPage, None),
    pytest.mark.skip_if_not_firefox((SmartOnBasePage, {'slug': 'tracking'}),
        reason='Newsletter is only shown to Firefox browsers.'),
    pytest.mark.skip_if_not_firefox((SmartOnBasePage, {'slug': 'security'}),
        reason='Newsletter is only shown to Firefox browsers.'),
    pytest.mark.skip_if_not_firefox((SmartOnBasePage, {'slug': 'surveillance'}),
        reason='Newsletter is only shown to Firefox browsers.')])
def test_newsletter_default_values(page_class, url_kwargs, base_url, selenium):
    url_kwargs = url_kwargs or {}
    page = page_class(selenium, base_url, **url_kwargs).open()
    page.newsletter.expand_form()
    assert '' == page.newsletter.email
    assert 'United States' == page.newsletter.country
    assert not page.newsletter.privacy_policy_accepted
    assert page.newsletter.is_privacy_policy_link_displayed


@pytest.mark.nondestructive
@pytest.mark.parametrize('page_class', [
    pytest.mark.skipif(HomePage, reason='https://bugzilla.mozilla.org/show_bug.cgi?id=1443566'),
    ContributePage,
    AboutPage])
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
    pytest.mark.skipif(HomePage, reason='https://bugzilla.mozilla.org/show_bug.cgi?id=1443566'),
    ContributePage,
    AboutPage])
def test_newsletter_sign_up_fails_when_missing_required_fields(page_class, base_url, selenium):
    page = page_class(selenium, base_url).open()
    page.newsletter.expand_form()
    with pytest.raises(TimeoutException):
        page.newsletter.click_sign_me_up()
