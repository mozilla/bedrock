# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.styleguide import StyleGuidePage


@pytest.mark.sanity
@pytest.mark.nondestructive
def test_open_close_navigation(base_url, selenium):
    page = StyleGuidePage(base_url, selenium).open()
    identity = page.menu[0]
    identity.expand()
    assert identity.is_displayed
    mozilla = identity.sub_menu[0]
    mozilla.expand()
    assert mozilla.is_displayed
    firefox_family = identity.sub_menu[1]
    firefox_family.expand()
    assert not mozilla.is_displayed
    assert firefox_family.is_displayed
    identity.collapse()
    assert not identity.is_displayed
    assert not firefox_family.is_displayed
