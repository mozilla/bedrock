# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage
from pages.regions.download_button import DownloadButton


class HelloPage(FirefoxBasePage):

    _url = '{base_url}/{locale}/firefox/hello'

    _try_hello_header_locator = (By.CSS_SELECTOR, '#try-hello .try-hello-button')
    _try_hello_footer_locator = (By.CSS_SELECTOR, '#share-hello .try-hello-button')
    _primary_download_locator = (By.ID, 'download-fx-primary')
    _secondary_download_locator = (By.ID, 'download-fx-secondary')

    @property
    def is_try_hello_header_button_displayed(self):
        return self.is_element_displayed(self._try_hello_header_locator)

    @property
    def is_try_hello_footer_button_displayed(self):
        return self.is_element_displayed(self._try_hello_footer_locator)

    @property
    def primary_download_button(self):
        el = self.find_element(self._primary_download_locator)
        return DownloadButton(self, root=el)

    @property
    def secondary_download_button(self):
        el = self.find_element(self._secondary_download_locator)
        return DownloadButton(self, root=el)
