# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.nightly import FirstRunPage


@pytest.mark.nondestructive
def test_first_run(base_url, selenium):
    page = FirstRunPage(selenium, base_url).open()
    assert page.is_start_testing_displayed
    assert page.is_start_coding_displayed
    assert page.is_start_localizing_displayed
