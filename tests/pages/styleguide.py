# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from base import BasePage
from page import PageRegion


class StyleGuidePage(BasePage):

    _url = '{base_url}/{locale}/styleguide'

    _sidebar_locator = (By.CSS_SELECTOR, '#sidebar nav > ul > .has-children')

    @property
    def menu(self):
        return [NavigationMenu(self.base_url, self.selenium, root=el) for el in
                self.find_elements(self._sidebar_locator)]


class NavigationMenu(PageRegion):

    _link_locator = (By.CLASS_NAME, 'toggle')
    _menu_locator = (By.CSS_SELECTOR, 'ul > li')
    _sub_menu_locator = (By.CSS_SELECTOR, 'ul > .has-children')

    @property
    def sub_menu(self):
        return [NavigationMenu(self.base_url, self.selenium, root=el) for el in
                self.find_elements(self._sub_menu_locator)]

    def expand(self):
        assert not self.is_displayed, 'Menu is already displayed'
        self.find_element(self._link_locator).click()
        self.wait.until(lambda m: self._root.get_attribute('aria-expanded') == 'true')

    def collapse(self):
        assert self.is_displayed, 'Menu is already hidden'
        self.find_element(self._link_locator).click()
        self.wait.until(lambda m: self._root.get_attribute('aria-expanded') == 'false')

    @property
    def is_displayed(self):
        return self.is_element_displayed(self._menu_locator)
