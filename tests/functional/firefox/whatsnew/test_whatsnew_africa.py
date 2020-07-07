# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.whatsnew.whatsnew_africa import FirefoxWhatsNewAfricaPage


@pytest.mark.skip_if_not_firefox(reason='Whatsnew pages are shown to Firefox only.')
@pytest.mark.nondestructive
def test_africa_qr_code_displayed(base_url, selenium):
    page = FirefoxWhatsNewAfricaPage(selenium, base_url).open()
    assert page.is_qr_code_displayed
