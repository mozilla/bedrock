# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.regions.download_button import DownloadButton
from pages.regions.menu_list import MenuList


class BrowserComparisonPage(BasePage):
    _URL_TEMPLATE = "/{locale}/firefox/browsers/compare/{slug}/"

    _primary_download_button_locator = (By.ID, "download-button-thanks")
    _secondary_download_button_locator = (By.ID, "download-secondary")
    _browser_menu_list_locator = (By.CSS_SELECTOR, ".mzp-c-menu-list.mzp-t-download")

    @property
    def primary_download_button(self):
        el = self.find_element(*self._primary_download_button_locator)
        return DownloadButton(self, root=el)

    @property
    def secondary_download_button(self):
        el = self.find_element(*self._secondary_download_button_locator)
        return DownloadButton(self, root=el)

    @property
    def browser_menu_list(self):
        el = self.find_element(*self._browser_menu_list_locator)
        return MenuList(self, root=el)
