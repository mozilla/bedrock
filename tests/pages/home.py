# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.regions.download_button import DownloadButton


class HomePage(BasePage):

    _download_button_locator = (By.ID, 'global-nav-download-firefox')
    _get_firefox_link_locator = (By.ID, 'fx-download-link')

    @property
    def download_button(self):
        el = self.find_element(*self._download_button_locator)
        return DownloadButton(self, root=el)

    @property
    def is_get_firefox_link_displayed(self):
        return self.is_element_displayed(*self._get_firefox_link_locator)
