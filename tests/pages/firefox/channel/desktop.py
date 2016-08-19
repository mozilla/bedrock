# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage
from pages.regions.download_button import DownloadButton


class ChannelDesktopPage(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/channel/desktop/'

    _beta_download_locator = (By.ID, 'desktop-beta-download')
    _developer_download_locator = (By.ID, 'desktop-developer-download')
    _nightly_download_locator = (By.ID, 'desktop-nightly-download')

    @property
    def beta_download_button(self):
        el = self.find_element(*self._beta_download_locator)
        return DownloadButton(self, root=el)

    @property
    def developer_download_button(self):
        el = self.find_element(*self._developer_download_locator)
        return DownloadButton(self, root=el)

    @property
    def nightly_download_button(self):
        el = self.find_element(*self._nightly_download_locator)
        return DownloadButton(self, root=el)
