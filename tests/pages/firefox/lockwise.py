# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage
from pages.regions.download_button import DownloadButton


class LockwisePage(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/lockwise/'

    _app_store_button_locator = (By.CSS_SELECTOR, '.mobile-download-buttons > a[data-cta-text="apple-app-store"]')
    _play_store_button_locator = (By.CSS_SELECTOR, '.mobile-download-buttons > a[data-cta-text="google-play-store"]')
    _download_button_locator = (By.ID, 'download-button-desktop-release')

    @property
    def is_app_store_button_displayed(self):
        return self.is_element_displayed(*self._app_store_button_locator)

    @property
    def is_play_store_button_displayed(self):
        return self.is_element_displayed(*self._play_store_button_locator)

    @property
    def download_button(self):
        el = self.find_element(*self._download_button_locator)
        return DownloadButton(self, root=el)
