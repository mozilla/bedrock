# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.whatsnew.whatsnew_id import FirefoxWhatsNewIDPage


@pytest.mark.skip_if_not_firefox(reason='Whatsnew pages are shown to Firefox only.')
@pytest.mark.nondestructive
def test_firefox_lite_qr_code(base_url, selenium):
    page = FirefoxWhatsNewIDPage(selenium, base_url).open()
    assert page.is_firefox_lite_qr_code_displayed
