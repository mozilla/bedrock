# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage
from pages.regions.download_button import DownloadButton


class FirefoxNotesPage(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/releasenotes/'

    _html_locator = (By.CSS_SELECTOR, 'html')
    _product_logo_locator = (By.CSS_SELECTOR, '.masthead h2 img')
    _version_locator = (By.CSS_SELECTOR, 'version > h2')
    _channel_name_locator = (By.CSS_SELECTOR, 'version > h3')
    _download_button_locator = (By.CSS_SELECTOR, '.download-list > li:first-child a')
    _download_all_locator = (By.CSS_SELECTOR, '.all-download a')

    @property
    def version(self):
        el = self.find_element(*self._version_locator)
        return el.textContent

    @property
    def channel(self):
        el = self.find_element(*self._channel_name_locator)
        return el.textContent

    @property
    def gtm_id(self):
        el = self.find_element(*self._html_locator)
        return el.get_attribute('data-gtm-page-id')

    @property
    def download_button_text(self):
        el = self.find_element(*self._download_button_locator)
        return el.textContent

    @property
    def download_button_link(self):
        el = self.find_element(*self._download_button_locator)
        return el.get_attribute('href')

    @property
    def logo(self):
        el = self.find_element(*self._product_logo_locator)
        return el.get_attribute('src')

    @property
    def download_all_url(self):
        el = self.find_element(*self._download_all_locator)
        return el.get_attribute('src')
