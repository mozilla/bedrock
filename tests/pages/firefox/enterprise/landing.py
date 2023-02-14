# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.regions.menu_list import MenuList


class EnterprisePage(BasePage):
    _URL_TEMPLATE = "/{locale}/firefox/enterprise/"

    _primary_download_button_locator = (By.ID, "primary-download-button")
    _win64_download_list_locator = (By.ID, "win64-download-list")
    _win32_download_list_locator = (By.ID, "win32-download-list")
    _mac_download_list_locator = (By.ID, "mac-download-list")

    @property
    def is_primary_download_button_displayed(self):
        return self.is_element_displayed(*self._primary_download_button_locator)

    @property
    def win64_download_list(self):
        el = self.find_element(*self._win64_download_list_locator)
        return MenuList(self, root=el)

    @property
    def win32_download_list(self):
        el = self.find_element(*self._win32_download_list_locator)
        return MenuList(self, root=el)

    @property
    def mac_download_list(self):
        el = self.find_element(*self._mac_download_list_locator)
        return MenuList(self, root=el)
