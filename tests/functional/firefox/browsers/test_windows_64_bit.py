# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.browsers.windows_64_bit import Windows64BitPage


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_download_button_is_displayed(base_url, selenium):
    page = Windows64BitPage(selenium, base_url).open()
    assert page.download_button.is_displayed


@pytest.mark.skip_if_firefox(reason='Sticky promo is displayed only to non-Firefox users')
@pytest.mark.nondestructive
def test_sticky_promo(base_url, selenium):
    page = Windows64BitPage(selenium, base_url).open()
    assert page.promo.is_displayed
    page.promo.close()
    assert not page.promo.is_displayed
