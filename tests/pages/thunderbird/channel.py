# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.regions.download_button import DownloadButton


class ThunderbirdChannelPage(BasePage):

    _url = '{base_url}/{locale}/thunderbird/channel'

    _earlybird_download_button_locator = (By.ID, 'download-button-desktop-alpha')
    _beta_download_button_locator = (By.ID, 'download-button-desktop-beta')

    @property
    def beta_download_button(self):
        el = self.find_element(self._beta_download_button_locator)
        return DownloadButton(self, root=el)

    @property
    def earlybird_download_button(self):
        el = self.find_element(self._earlybird_download_button_locator)
        return DownloadButton(self, root=el)
