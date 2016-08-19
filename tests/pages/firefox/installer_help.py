# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage
from pages.regions.download_button import DownloadButton


class InstallerHelpPage(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/installer-help/'

    _firefox_download_button_locator = (By.ID, 'download-button-desktop-release')
    _beta_download_button_locator = (By.ID, 'download-button-desktop-beta')
    _dev_edition_download_button_locator = (By.ID, 'download-button-desktop-alpha')
    _nightly_download_button_locator = (By.ID, 'download-button-desktop-nightly')

    @property
    def firefox_download_button(self):
        el = self.find_element(*self._firefox_download_button_locator)
        return DownloadButton(self, root=el)

    @property
    def beta_download_button(self):
        el = self.find_element(*self._beta_download_button_locator)
        return DownloadButton(self, root=el)

    @property
    def dev_edition_download_button(self):
        el = self.find_element(*self._dev_edition_download_button_locator)
        return DownloadButton(self, root=el)

    @property
    def nightly_download_button(self):
        el = self.find_element(*self._nightly_download_button_locator)
        return DownloadButton(self, root=el)
