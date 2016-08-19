# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected

from pages.firefox.base import FirefoxBaseRegion


class SendToDevice(FirefoxBaseRegion):

    _root_locator = (By.ID, 'send-to-device')
    _email_locator = (By.ID, 'id-input')
    _submit_button_locator = (By.CSS_SELECTOR, '.form-submit > button')
    _thank_you_locator = (By.CSS_SELECTOR, '.thank-you')

    def type_email(self, value):
        self.find_element(*self._email_locator).send_keys(value)

    def click_send(self):
        self.scroll_element_into_view(*self._submit_button_locator).click()
        self.wait.until(expected.visibility_of_element_located(self._thank_you_locator))

    @property
    def send_successful(self):
        el = self.selenium.find_element(*self._thank_you_locator)
        return el.is_displayed()

    @property
    def is_displayed(self):
        return self.page.is_element_displayed(*self._root_locator)
