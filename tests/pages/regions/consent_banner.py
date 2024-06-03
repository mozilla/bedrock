# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from pypom import Region
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected


class ConsentBanner(Region):
    _root_locator = (By.ID, "moz-consent-banner")
    _accept_button_locator = (By.ID, "moz-consent-banner-button-accept")
    _reject_button_locator = (By.ID, "moz-consent-banner-button-reject")

    @property
    def is_displayed(self):
        return self.page.is_element_displayed(*self._root_locator)

    def click_accept_button(self):
        accept_cookie_button = self.find_element(*self._accept_button_locator)
        self.wait.until(expected.element_to_be_clickable(accept_cookie_button))
        accept_cookie_button.click()
        self.wait.until(lambda s: self.is_displayed is False)

    def click_reject_button(self):
        reject_cookie_button = self.find_element(*self._reject_button_locator)
        self.wait.until(expected.element_to_be_clickable(reject_cookie_button))
        reject_cookie_button.click()
        self.wait.until(lambda s: self.is_displayed is False)
