# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage


class ThankYouPage(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/new/?scene=2'

    _direct_download_link_locator = (By.ID, 'direct-download-link')

    @property
    def is_direct_download_link_displayed(self):
        return self.is_element_displayed(*self._direct_download_link_locator)

    @property
    def is_direct_download_link_valid(self):
        return 'https://download.mozilla.org' in self.find_element(
            *self._direct_download_link_locator).get_attribute('href')
