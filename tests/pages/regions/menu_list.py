# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BaseRegion


class MenuList(BaseRegion):

    _title_button_locator = (By.CSS_SELECTOR, ".mzp-c-menu-list-title > button")
    _list_locator = (By.CSS_SELECTOR, ".mzp-c-menu-list-list")

    # Elements on page to make are added to window.dataLayer after click
    _browser_menu_desktop_download_link_locator = (By.CSS_SELECTOR, ".mzp-c-menu-list-item a[data-link-type=Desktop]")
    _browser_menu_android_download_link_locator = (By.CSS_SELECTOR, ".mzp-c-menu-list-item a[data-link-type=Desktop]")
    _browser_menu_ios_download_link_locator = (By.CSS_SELECTOR, ".mzp-c-menu-list-item a[data-link-type=Desktop]")

    # list is visible

    @property
    def list_is_open(self):
        return self.page.is_element_displayed(*self._list_locator)

    def click(self):
        self.scroll_element_into_view(*self._title_button_locator).click()

    @property
    def desktop_download(self):
        return self.find_element(*self._browser_menu_desktop_download_link_locator)

    def desktop_download_click(self):
        self.scroll_element_into_view(*self._title_button_locator).click()
        self.find_element(*self._browser_menu_desktop_download_link_locator).click()

    @property
    def android_download(self):
        return self.find_element(*self._browser_menu_android_download_link_locator)

    @property
    def ios_download(self):
        return self.find_element(*self._browser_menu_ios_download_link_locator)
