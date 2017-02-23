# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pypom import Region
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected

from pages.base import BasePage


class ScrollElementIntoView(object):

    def scroll_element_into_view(self, strategy, locator):
        # scroll elements so they are not beneath the header
        offset = {'x': 0, 'y': -100}
        return super(ScrollElementIntoView, self).scroll_element_into_view(
            strategy, locator, **offset)


class FirefoxBaseRegion(ScrollElementIntoView, Region):
    pass


class FirefoxBasePage(ScrollElementIntoView, BasePage):

    @property
    def family_navigation(self):
        return self.FamilyNavigation(self)

    class FamilyNavigation(FirefoxBaseRegion):

        _root_locator = (By.ID, 'fxfamilynav-header')
        _active_primary_nav_locator = (By.CSS_SELECTOR, '#fxfamilynav-primary li.active a')
        _adjunct_nav_button_locator = (By.ID, 'fxfamilynav-adjunctnav-trigger')
        _adjunct_nav_menu_locator = (By.ID, 'fxfamilynav-adjunctnav')

        def open_adjunct_menu(self):
            self.find_element(*self._adjunct_nav_button_locator).click()
            self.wait.until(expected.visibility_of_element_located(self._adjunct_nav_menu_locator))

        @property
        def is_adjunct_menu_displayed(self):
            return self.is_element_displayed(*self._adjunct_nav_menu_locator)

        @property
        def active_primary_nav_id(self):
            return self.find_element(*self._active_primary_nav_locator).get_attribute('data-id')
