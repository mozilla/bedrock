# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.new.sticky_promo import StickyPromo


@pytest.mark.smoke
@pytest.mark.sanity
@pytest.mark.nondestructive
def test_sticky_promo_displayed(base_url, selenium):
    page = StickyPromo(selenium, base_url, params='').open()
    assert page.is_sticky_promo_displayed

#
# @pytest.mark.nondestructive
# @pytest.mark.skip_if_not_firefox(reason='Join Firefox form is only displayed to Firefox users')
# def test_sticky_promo_modal(base_url, selenium):
#     page = StickyPromo(selenium, base_url, params='').open()
#     modal = page.open_sticky_promo_modal()
#     assert modal.is_displayed
#     modal.close()
