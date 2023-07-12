# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.whatsnew.whatsnew_116 import FirefoxWhatsNew116Page


@pytest.mark.skip_if_not_firefox(reason="Whatsnew pages are shown to Firefox only.")
@pytest.mark.nondestructive
@pytest.mark.parametrize("locale", [("de"), ("fr"), ("en-GB"), ("en-US")])
def test_firefox_default_button_displayed(locale, base_url, selenium):
    page = FirefoxWhatsNew116Page(selenium, base_url, locale=locale).open()
    assert page.is_firefox_default_button_displayed
