# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.manifesto import ManifestoPage


@pytest.mark.nondestructive
def test_share_button_is_displayed(base_url, selenium):
    page = ManifestoPage(selenium, base_url).open()
    assert page.is_primary_share_button_displayed
    assert page.is_secondary_share_button_displayed
