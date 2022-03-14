# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.new.download_yandex import YandexDownloadPage


@pytest.mark.skip(reason="Switch disabled")
@pytest.mark.smoke
@pytest.mark.nondestructive
def test_download_buttons_are_displayed(base_url, selenium):
    page = YandexDownloadPage(selenium, base_url, locale="ru", params="?geo=us").open()
    assert page.is_download_button_displayed
    assert not page.is_yandex_download_button_displayed


@pytest.mark.skip(reason="Switch disabled")
@pytest.mark.nondestructive
@pytest.mark.skip_if_not_firefox(reason="Join Firefox form is only displayed to Firefox users")
def test_firefox_account_modal(base_url, selenium):
    page = YandexDownloadPage(selenium, base_url, locale="ru", params="?geo=us").open()
    modal = page.open_join_firefox_modal()
    assert modal.is_displayed
    modal.close()


@pytest.mark.skip(reason="Switch disabled")
@pytest.mark.smoke
@pytest.mark.nondestructive
def test_yandex_download_button_displayed(base_url, selenium):
    page = YandexDownloadPage(selenium, base_url, locale="ru", params="?geo=ru").open()
    assert not page.is_download_button_displayed
    assert page.is_yandex_download_button_displayed
