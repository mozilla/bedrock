# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage
from pages.regions.download_button import DownloadButton


class FirefoxAccountsPage(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/accounts/'

    _download_button_locator = (By.ID, 'download-button-desktop-release')
    _accounts_form_locator = (By.ID, 'fxa-iframe-config')

    @property
    def download_button(self):
        el = self.find_element(*self._download_button_locator)
        return DownloadButton(self, root=el)

    @property
    def is_accounts_form_displayed(self):
        return self.is_element_displayed(*self._accounts_form_locator)
