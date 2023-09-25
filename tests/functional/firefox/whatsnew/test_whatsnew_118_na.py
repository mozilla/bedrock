# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.whatsnew.whatsnew_118_na import FirefoxWhatsNew118NAPage


@pytest.mark.skip_if_not_firefox(reason="Whatsnew pages are shown to Firefox only.")
@pytest.mark.nondestructive
@pytest.mark.parametrize("locale", [("en-US"), ("en-CA")])
def test_firefox_try_it_button_displayed(locale, base_url, selenium):
    page = FirefoxWhatsNew118NAPage(selenium, base_url, locale=locale).open()
    assert page.is_try_it_button_displayed
