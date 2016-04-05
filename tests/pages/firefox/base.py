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
        return self.FamilyNavigation(self)

    def scroll_element_into_view(self, locator):
        return super(FirefoxBasePage, self).scroll_element_into_view(
            locator, y=HEADER_OFFSET)

    class FamilyNavigation(PageRegion):

        _root_locator = (By.ID, 'fxfamilynav-header')
        _active_primary_nav_locator = (By.CSS_SELECTOR, '#fxfamilynav-primary li.active a')
        _adjunct_nav_button_locator = (By.ID, 'fxfamilynav-adjunctnav-trigger')
        _adjunct_nav_menu_locator = (By.ID, 'fxfamilynav-adjunctnav')

        def open_adjunct_menu(self):
            self.find_element(self._adjunct_nav_button_locator).click()
            self.wait.until(expected.visibility_of_element_located(self._adjunct_nav_menu_locator))

        @property
        def is_adjunct_menu_displayed(self):
            return self.is_element_displayed(self._adjunct_nav_menu_locator)

        @property
        def active_primary_nav_id(self):
            return self.find_element(self._active_primary_nav_locator).get_attribute('data-id')


class FirefoxBasePageRegion(PageRegion):

    def scroll_element_into_view(self, locator):
        return super(FirefoxBasePageRegion, self).scroll_element_into_view(
            locator, y=HEADER_OFFSET)
