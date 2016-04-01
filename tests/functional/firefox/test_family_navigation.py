# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.family_navigation import FirefoxPage


@pytest.mark.nondestructive
@pytest.mark.parametrize('slug', [
    pytest.mark.smoke(('android')),
    pytest.mark.smoke(('desktop')),
    pytest.mark.smoke(('ios')),
    pytest.mark.smoke(('features'))])
def test_family_navigation_active_nav(slug, base_url, selenium):
    page = FirefoxPage(base_url, selenium, slug=slug).open()
    assert page.family_navigation.active_primary_nav_id == slug


@pytest.mark.nondestructive
@pytest.mark.parametrize('slug', [
    pytest.mark.smoke(('android')),
    pytest.mark.smoke(('desktop')),
    ('desktop/customize'),
    ('desktop/fast'),
    ('desktop/trust'),
    ('dnt'),
    ('interest-dashboard'),
    pytest.mark.smoke(('ios'))])
def test_family_navigation_adjunct_menu(slug, base_url, selenium):
    page = FirefoxPage(base_url, selenium, slug=slug).open()
    page.family_navigation.open_adjunct_menu()
    assert page.family_navigation.is_adjunct_menu_displayed
