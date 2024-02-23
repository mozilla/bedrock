# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.regions.join_firefox_form import JoinFirefoxForm
from pages.regions.menu_list import MenuList


class ProductsPage(BasePage):
    _URL_TEMPLATE = "/{locale}/products/"

    _firefox_menu_list_locator = (By.ID, "menu-browsers-wrapper")
    _focus_menu_list_locator = (By.ID, "menu-focus-wrapper")
    _pocket_menu_list_locator = (By.ID, "menu-pocket-wrapper")

    @property
    def firefox_menu_list(self):
        el = self.find_element(*self._firefox_menu_list_locator)
        return MenuList(self, root=el)

    @property
    def focus_menu_list(self):
        el = self.find_element(*self._focus_menu_list_locator)
        return MenuList(self, root=el)

    @property
    def pocket_menu_list(self):
        el = self.find_element(*self._pocket_menu_list_locator)
        return MenuList(self, root=el)

    @property
    def join_firefox_form(self):
        return JoinFirefoxForm(self)
