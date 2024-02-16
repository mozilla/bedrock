# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected

from pages.base import BasePage


class OptOutConfirmationPage(BasePage):
    _URL_TEMPLATE = "/{locale}/newsletter/opt-out-confirmation/"

    _email_locator = (By.ID, "id_email")
    _submit_button_locator = (By.ID, "newsletter-submit")
    _success_message_locator = (By.CLASS_NAME, "newsletter-recovery-form-success-msg")
    _error_message_locator = (By.CLASS_NAME, "error-try-again-later")

    def type_email(self, value):
        self.find_element(*self._email_locator).send_keys(value)

    def click_submit(self, expected_result=None):
        self.find_element(*self._submit_button_locator).click()
        if expected_result == "error":
            self.wait.until(expected.visibility_of_element_located(self._error_message_locator))
        else:
            self.wait.until(expected.visibility_of_element_located(self._success_message_locator))

    @property
    def is_success_message_displayed(self):
        return self.is_element_displayed(*self._success_message_locator)

    @property
    def is_error_message_displayed(self):
        return self.is_element_displayed(*self._error_message_locator)
