# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.not_found import NotFoundPage


@pytest.mark.nondestructive
def test_is_download_button_displayed(base_url, selenium):
    page = NotFoundPage(selenium, base_url).open()
    assert page.download_button.is_displayed
