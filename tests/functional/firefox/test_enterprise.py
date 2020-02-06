# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.enterprise.landing import EnterprisePage


@pytest.mark.nondestructive
def test_primary_download_button_displayed(base_url, selenium):
    page = EnterprisePage(selenium, base_url).open()
    assert page.is_primary_download_button_displayed
