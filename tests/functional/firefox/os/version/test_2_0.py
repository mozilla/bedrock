# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.os.version.v2_0 import FirefoxOSPage


@pytest.mark.sanity
@pytest.mark.nondestructive
def test_app_category_selector(base_url, selenium):
    page = FirefoxOSPage(base_url, selenium).open()
    for group in page.app_groups:
        group.select()
        assert group.is_active
