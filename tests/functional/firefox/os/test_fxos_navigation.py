# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.family_navigation import FirefoxPage


@pytest.mark.nondestructive
@pytest.mark.parametrize('slug', [
    pytest.mark.smoke(('os')),
    pytest.mark.smoke(('os/devices')),
    pytest.mark.smoke(('os/devices/tv'))])
def test_fxos_navigation_active_nav(slug, base_url, selenium):
    page = FirefoxPage(base_url, selenium, slug=slug).open()
    assert page.fxos_navigation.active_primary_nav_id == slug.replace('/', '-')


@pytest.mark.nondestructive
@pytest.mark.parametrize('slug', [
    pytest.mark.smoke(('os')),
    pytest.mark.smoke(('os/devices')),
    pytest.mark.smoke(('os/devices/tv'))])
def test_fxos_navigation_adjunct_menu(slug, base_url, selenium):
    page = FirefoxPage(base_url, selenium, slug=slug).open()
    page.fxos_navigation.open_adjunct_menu()
    assert page.fxos_navigation.is_adjunct_menu_displayed
