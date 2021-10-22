# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.not_found import NotFoundPage


@pytest.mark.nondestructive
def test_go_back_button_is_displayed_with_history(base_url, selenium):
    selenium.get(base_url)
    page = NotFoundPage(selenium, base_url).open()
    assert page.is_go_back_button_displayed
