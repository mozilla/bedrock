# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.new.download import DownloadPage


@pytest.mark.nondestructive
def test_download_button_displayed(base_url, selenium):
    page = DownloadPage(selenium, base_url, locale='ru', params='?geo=us').open()
    assert page.download_button.is_displayed
    assert not page.is_yandex_download_button_displayed


@pytest.mark.nondestructive
def test_yandex_download_button_displayed(base_url, selenium):
    page = DownloadPage(selenium, base_url, locale='ru', params='?geo=ru').open()
    assert not page.download_button.is_displayed
    assert page.is_yandex_download_button_displayed


@pytest.mark.nondestructive
def test_other_platforms_modal(base_url, selenium):
    page = DownloadPage(selenium, base_url, locale='ru', params='?geo=us').open()
    modal = page.open_other_platforms_modal()
    assert modal.is_displayed
    modal.close()
