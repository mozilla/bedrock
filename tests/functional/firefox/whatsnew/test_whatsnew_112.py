# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.whatsnew.whatsnew_112 import FirefoxWhatsNew112Page


@pytest.mark.skip_if_not_firefox(reason="Whatsnew pages are shown to Firefox only.")
@pytest.mark.nondestructive
@pytest.mark.parametrize("locale", [("de"), ("fr"), ("en-GB")])
def test_set_default_button_displayed(locale, base_url, selenium):
    page = FirefoxWhatsNew112Page(selenium, base_url, locale=locale).open()
    assert page.is_firefox_set_default_button_displayed
    assert not page.is_firefox_protection_report_button_displayed
