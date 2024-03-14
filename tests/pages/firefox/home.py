# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.regions.menu_list import MenuList


class FirefoxHomePage(BasePage):
    _URL_TEMPLATE = "/{locale}/firefox/"

    # browser download menu list
    _browser_menu_list_locator = (By.ID, "test-menu-browsers-wrapper")

    # facebook container extension link visibility
    _facebook_container_link_locator = (By.ID, "test-fbc")

    @property
    def fb_container_is_displayed(self):
        return self.is_element_displayed(*self._facebook_container_link_locator)

    @property
    def browser_menu_list(self):
        el = self.find_element(*self._browser_menu_list_locator)
        return MenuList(self, root=el)
