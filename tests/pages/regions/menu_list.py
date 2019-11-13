# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pypom import Region
from selenium.webdriver.common.by import By


class MenuList(Region):

    _title_button_locator = (By.CSS_SELECTOR, '.mzp-c-menu-list-title > button')
    _list_locator = (By.CSS_SELECTOR, '.mzp-c-menu-list-list')

    # list is visible

    @property
    def list_is_open(self):
        return self.page.is_element_displayed(*self._list_locator)

    def click(self):
        self.scroll_element_into_view(*self._title_button_locator)
        self.find_element(*self._title_button_locator).click()
