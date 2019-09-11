# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.lean_data import LeanDataPage


@pytest.mark.nondestructive
@pytest.mark.parametrize('slug', [
    ('/'),
    ('/stay-lean/'),
    ('/build-security/'),
    ('/engage-users/')])
def test_contact_button_is_displayed(slug, base_url, selenium):
    page = LeanDataPage(selenium, base_url, slug=slug).open()
    assert page.is_contact_button_displayed
