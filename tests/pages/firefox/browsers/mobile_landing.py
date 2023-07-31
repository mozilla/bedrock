# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.regions.menu_list import MenuList


class FirefoxMobilePage(BasePage):
    _URL_TEMPLATE = "/{locale}/firefox/browsers/mobile/"

    _android_download_link_locator = (By.ID, "android-download")
    _ios_download_link_locator = (By.ID, "ios-download")
    _focus_menu_list_locator = (By.ID, "menu-focus-wrapper")

    @property
    def focus_menu_list(self):
        el = self.find_element(*self._focus_menu_list_locator)
        return MenuList(self, root=el)

    @property
    def is_android_download_link_displayed(self):
        return self.is_element_displayed(*self._android_download_link_locator)

    @property
    def is_ios_download_link_displayed(self):
        return self.is_element_displayed(*self._ios_download_link_locator)
