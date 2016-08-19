# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pypom import Region
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected


class Modal(Region):

    _root_locator = (By.ID, 'modal')
    _close_locator = (By.ID, 'modal-close')

    def close(self):
        modal = self.selenium.find_element(*self._root_locator)
        self.find_element(*self._close_locator).click()
        self.wait.until(expected.staleness_of(modal))

    @property
    def is_displayed(self):
        return self.page.is_element_displayed(*self._root_locator)

    def displays(self, selector):
        return self.is_element_displayed(*selector)
