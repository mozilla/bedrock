# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.regions.download_button import DownloadButton


class HomePage(BasePage):

    _intro_download_button_locator = (By.ID, 'download-intro')  # legacy home page
    _primary_download_button_locator = (By.ID, 'download-primary')
    _secondary_download_button_locator = (By.ID, 'download-secondary')
    _primary_accounts_button_locator = (By.ID, 'fxa-learn-primary')
    _secondary_accounts_button_locator = (By.ID, 'fxa-learn-secondary')

    @property
    def intro_download_button(self):
        el = self.find_element(*self._intro_download_button_locator)
        return DownloadButton(self, root=el)

    @property
    def primary_download_button(self):
        el = self.find_element(*self._primary_download_button_locator)
        return DownloadButton(self, root=el)

    @property
    def secondary_download_button(self):
        el = self.find_element(*self._secondary_download_button_locator)
        return DownloadButton(self, root=el)

    @property
    def is_primary_accounts_button(self):
        return self.is_element_displayed(*self._primary_accounts_button_locator)

    @property
    def is_secondary_accounts_button(self):
        return self.is_element_displayed(*self._secondary_accounts_button_locator)
