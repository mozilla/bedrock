# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.new.sticky_promo import StickyPromoPage


@pytest.mark.nondestructive
def test_sticky_promo(base_url, selenium):
    page = StickyPromoPage(selenium, base_url).open()
    assert page.promo.is_displayed
    page.promo.close()
    assert not page.promo.is_displayed
