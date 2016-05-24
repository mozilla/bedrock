# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected

from pages.firefox.base import FirefoxBasePage, FirefoxBaseRegion


class ProductsPage(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/products'

    @property
    def download_bar(self):
        return self.DownloadBar(self)

    class DownloadBar(FirefoxBaseRegion):

        _root_locator = (By.ID, 'conditional-download-bar')
        _download_firefox_message_locator = (By.ID, 'dlbar-nonfx')
        _close_button_locator = (By.CLASS_NAME, 'btn-close')

        @property
        def is_displayed(self):
            return self.is_element_displayed(*self._root_locator)

        @property
        def is_download_firefox_message_displayed(self):
            return self.is_element_displayed(*self._download_firefox_message_locator)

        def close(self):
            download_bar = self.selenium.find_element(*self._root_locator)
            self.find_element(*self._close_button_locator).click()
            self.wait.until(expected.staleness_of(download_bar))
