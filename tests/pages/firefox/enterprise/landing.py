# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage


class EnterprisePage(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/enterprise/'

    _primary_download_button_locator = (By.ID, 'primary-download-button')
    _win64_download_list_locator = (By.CSS_SELECTOR, '#win64-download-list.is-details')
    _win32_download_list_locator = (By.CSS_SELECTOR, '#win32-download-list.is-details')
    _mac_download_list_locator = (By.CSS_SELECTOR, '#mac-download-list.is-details')

    @property
    def is_primary_download_button_displayed(self):
        return self.is_element_displayed(*self._primary_download_button_locator)

    @property
    def is_win64_download_list_displayed(self):
        return self.is_element_displayed(*self._win64_download_list_locator)

    @property
    def is_win32_download_list_displayed(self):
        return self.is_element_displayed(*self._win32_download_list_locator)

    @property
    def is_mac_download_list_displayed(self):
        return self.is_element_displayed(*self._mac_download_list_locator)
