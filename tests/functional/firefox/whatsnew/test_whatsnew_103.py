# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.whatsnew.whatsnew_103 import FirefoxWhatsNew103Page


@pytest.mark.skip_if_not_firefox(reason="Whatsnew pages are shown to Firefox only.")
@pytest.mark.nondestructive
@pytest.mark.parametrize("locale", [("en-US"), ("en-GB"), ("de"), ("fr")])
def test_firefox_default_button_is_displayed(locale, base_url, selenium):
    page = FirefoxWhatsNew103Page(selenium, base_url, locale=locale, params="?geo=gb").open()
    assert page.is_firefox_default_button_displayed
    assert not page.is_firefox_default_success_message_displayed
