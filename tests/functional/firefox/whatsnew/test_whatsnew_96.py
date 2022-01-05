# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.whatsnew.whatsnew_96 import FirefoxWhatsNew96Page


@pytest.mark.skip_if_not_firefox(reason="Whatsnew pages are shown to Firefox only.")
@pytest.mark.nondestructive
@pytest.mark.parametrize("locale", [("de"), ("fr")])
def test_relay_button_is_displayed_signed_in(locale, base_url, selenium):
    page = FirefoxWhatsNew96Page(selenium, base_url, locale=locale, params="?signed-in=true").open()
    assert page.is_relay_button_displayed_when_signed_in


@pytest.mark.skip_if_not_firefox(reason="Whatsnew pages are shown to Firefox only.")
@pytest.mark.nondestructive
@pytest.mark.parametrize("locale", [("de"), ("fr")])
def test_fxa_button_is_displayed_signed_out(locale, base_url, selenium):
    page = FirefoxWhatsNew96Page(selenium, base_url, locale=locale, params="?signed-in=false").open()
    assert page.is_fxa_button_displayed_when_signed_out
