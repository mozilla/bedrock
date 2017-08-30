# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.family_navigation import FirefoxPage


@pytest.mark.nondestructive
@pytest.mark.parametrize(('slug', 'locale'), [
    ('dnt', None),
    ('interest-dashboard', None)])
def test_family_navigation_active_nav(slug, locale, base_url, selenium):
    locale = locale or 'en-US'
    page = FirefoxPage(selenium, base_url, locale, slug=slug).open()
    assert page.family_navigation.active_primary_nav_id == 'desktop'


@pytest.mark.nondestructive
@pytest.mark.parametrize(('slug', 'locale'), [
    ('dnt', None),
    ('interest-dashboard', None)])
def test_family_navigation_adjunct_menu(slug, locale, base_url, selenium):
    locale = locale or 'en-US'
    page = FirefoxPage(selenium, base_url, locale, slug=slug).open()
    page.family_navigation.open_adjunct_menu()
    assert page.family_navigation.is_adjunct_menu_displayed
