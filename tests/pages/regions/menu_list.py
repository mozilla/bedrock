# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BaseRegion


class MenuList(BaseRegion):

    _title_button_locator = (By.CSS_SELECTOR, ".mzp-c-menu-list-title > button")
    _list_locator = (By.CSS_SELECTOR, ".mzp-c-menu-list-list")

    # list is visible

    @property
    def list_is_open(self):
        return self.page.is_element_displayed(*self._list_locator)

    def click(self):
        self.scroll_element_into_view(*self._title_button_locator).click()
