# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.contribute.friends import ContributeFriendsPage


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_display_signup_form(base_url, selenium):
    page = ContributeFriendsPage(base_url, selenium).open()
    page.click_show_signup_form()
    assert page.is_signup_form_displayed
