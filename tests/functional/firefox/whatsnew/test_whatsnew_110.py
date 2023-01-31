# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.whatsnew.whatsnew_110 import FirefoxWhatsNew110Page


@pytest.mark.skip_if_not_firefox(reason="Whatsnew pages are shown to Firefox only.")
@pytest.mark.nondestructive
@pytest.mark.parametrize("locale, params", [("de", "?v=1"), ("de", "?v=2"), ("fr", "?v=test"), ("en-GB", "?v=test")])
def test_pocket_button_is_displayed(locale, params, base_url, selenium):
    page = FirefoxWhatsNew110Page(selenium, base_url, locale=locale, params=params).open()
    assert page.is_pocket_button_displayed
