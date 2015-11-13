# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.ui import WebDriverWait as Wait

from pages.base import BasePage
from pages.page import PageRegion


class FirefoxBasePage(BasePage):

    def open_family_navigation_menu(self):
        navigation = self.FamilyNavigation(self.selenium)
        navigation.open_menu()
        return navigation

    class FamilyNavigation(PageRegion):

        _root_locator = (By.ID, 'fxfamilynav-header')
        _nav_button_locator = (By.ID, 'fxfamilynav-tertiarynav-trigger')
        _nav_menu_locator = (By.ID, 'fxfamilynav-tertiarynav')

        def open_menu(self):
            self.root.find_element(*self._nav_button_locator).click()
            Wait(self.selenium, self.timeout).until(
                expected.visibility_of_element_located(self._nav_menu_locator))

        @property
        def is_displayed(self):
            return self.is_element_displayed(self._nav_menu_locator)
