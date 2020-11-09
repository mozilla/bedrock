# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected

from pages.base import BaseRegion


class StickyPromo(BaseRegion):

    _root_locator = (By.CLASS_NAME, 'mzp-c-sticky-promo')
    _close_locator = (By.CLASS_NAME, 'mzp-c-sticky-promo-close')

    def close(self):
        stickyPromo = self.selenium.find_element(*self._root_locator)
        self.find_element(*self._close_locator).click()
        self.wait.until(expected.staleness_of(stickyPromo))

    @property
    def is_displayed(self):
        return self.page.is_element_displayed(*self._root_locator)

    def displays(self, selector):
        return self.is_element_displayed(*selector)


class StickyPromoProtocol(BaseRegion):

    _root_locator = (By.CLASS_NAME, 'mzp-c-sticky-promo')
    _close_locator = (By.CLASS_NAME, 'mzp-c-sticky-promo-close')

    def close(self):
        stickyPromo = self.selenium.find_element(*self._root_locator)
        self.find_element(*self._close_locator).click()
        self.wait.until(expected.staleness_of(stickyPromo))

    @property
    def is_displayed(self):
        return self.page.is_element_displayed(*self._root_locator)

    def displays(self, selector):
        return self.is_element_displayed(*selector)
