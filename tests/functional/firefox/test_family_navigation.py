# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.family_navigation import FirefoxPage


@pytest.mark.nondestructive
@pytest.mark.parametrize('slug', [
    pytest.mark.smoke(('android')),
    pytest.mark.smoke(('desktop')),
    ('desktop/customize/'),
    ('desktop/fast/'),
    ('desktop/trust/'),
    ('dnt'),
    pytest.mark.smoke(('hello')),
    ('interest-dashboard'),
    pytest.mark.smoke(('ios')),
    pytest.mark.smoke(('os/devices')),
    pytest.mark.smoke(('os/2.5')),
    ('os/2.0'),
    ('os/2.5'),
    ('os/1.4'),
    ('os/1.3t'),
    ('os/1.3'),
    ('os/1.1'),
    ('partners'),
    ('private-browsing'),
    ('push'),
    ('sync'),
    ('tiles')])
def test_family_navigation_menu(slug, base_url, selenium):
    page = FirefoxPage(base_url, selenium, slug=slug).open()
    page.family_navigation.open_menu()
    assert page.family_navigation.is_menu_displayed
