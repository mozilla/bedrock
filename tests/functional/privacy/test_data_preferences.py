# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.privacy.data_preferences import DataPreferencesPage


@pytest.mark.nondestructive
def test_data_preferences_opt_out(base_url, selenium):
    page = DataPreferencesPage(selenium, base_url).open()
    assert page.is_opt_in_status_shown
    page.click_opt_out()
    assert page.is_opt_out_status_shown
    page.click_opt_in()
    assert page.is_opt_in_status_shown
