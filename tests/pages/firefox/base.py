# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected

from pages.base import BasePage
from pages.page import PageRegion

# this should be enough to scroll elements so they are not beneath the header
HEADER_OFFSET = -100


class FirefoxBasePage(BasePage):

    @property
    def family_navigation(self):
        return self.FamilyNavigation(self.base_url, self.selenium)

    def scroll_element_into_view(self, locator):
        return super(FirefoxBasePage, self).scroll_element_into_view(
            locator, y=HEADER_OFFSET)

    class FamilyNavigation(PageRegion):

        _root_locator = (By.ID, 'fxfamilynav-header')
        _nav_button_locator = (By.ID, 'fxfamilynav-tertiarynav-trigger')
        _nav_menu_locator = (By.ID, 'fxfamilynav-tertiarynav')

        def open_menu(self):
            self.find_element(self._nav_button_locator).click()
            self.wait.until(expected.visibility_of_element_located(self._nav_menu_locator))

        @property
        def is_menu_displayed(self):
            return self.is_element_displayed(self._nav_menu_locator)


class FirefoxBasePageRegion(PageRegion):

    def scroll_element_into_view(self, locator):
        return super(FirefoxBasePageRegion, self).scroll_element_into_view(
            locator, y=HEADER_OFFSET)
