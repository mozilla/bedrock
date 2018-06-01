# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.home import HomePage


@pytest.mark.sanity
@pytest.mark.nondestructive
def test_download_button_is_displayed_en(base_url, selenium):
    page = HomePage(selenium, base_url).open()
    assert page.primary_download_button.is_displayed
    assert page.secondary_download_button.is_displayed


@pytest.mark.sanity
@pytest.mark.nondestructive
def test_download_button_is_displayed_locales(base_url, selenium):
    page = HomePage(selenium, base_url, locale='de').open()
    assert page.intro_download_button.is_displayed
