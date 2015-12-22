# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.os.version.all import FirefoxOSBasePage


@pytest.mark.nondestructive
@pytest.mark.parametrize('version', [
    pytest.mark.smoke(('2.5')),
    pytest.mark.smoke(('2.0')),
    ('1.4'),
    ('1.3t'),
    ('1.3'),
    ('1.1')])
def test_family_navigation(version, base_url, selenium):
    page = FirefoxOSBasePage(base_url, selenium, version=version).open()
    page.family_navigation.open_menu()
    assert page.family_navigation.is_menu_displayed


@pytest.mark.nondestructive
@pytest.mark.parametrize('version', [('2.0'), ('1.4'), ('1.3t'), ('1.3'), ('1.1')])
def test_news_is_displayed(version, base_url, selenium):
    page = FirefoxOSBasePage(base_url, selenium, version=version).open()
    assert page.is_news_displayed


@pytest.mark.nondestructive
@pytest.mark.parametrize('version', [
    pytest.mark.smoke(('2.0')),
    ('1.4'),
    ('1.3t'),
    ('1.3'),
    ('1.1')])
def test_call_to_action_buttons_are_present(version, base_url, selenium):
    page = FirefoxOSBasePage(base_url, selenium, version=version).open()
    # test for presence of buttons only as display is dependent upon geo location
    # TODO explore better ways to test this in the future?
    assert page.is_primary_signup_button_present
    assert page.is_primary_get_phone_button_present
