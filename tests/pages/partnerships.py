# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class PartnershipsPage(BasePage):

    URL_TEMPLATE = '/{locale}/about/partnerships/'

    _first_name_locator = (By.ID, 'first_name')
    _last_name_locator = (By.ID, 'last_name')
    _company_locator = (By.ID, 'company')
    _email_locator = (By.ID, 'email')
    _submit_request_locator = (By.ID, 'sf-form-submit')
    _thank_you_locator = (By.ID, 'partner-form-success')

    def type_first_name(self, value):
        self.find_element(*self._first_name_locator).send_keys(value)

    def type_last_name(self, value):
        self.find_element(*self._last_name_locator).send_keys(value)

    def type_company(self, value):
        self.find_element(*self._company_locator).send_keys(value)

    def type_email(self, value):
        self.find_element(*self._email_locator).send_keys(value)

    def submit_request(self):
        self.find_element(*self._submit_request_locator).click()
        self.wait.until(lambda s: self.request_successful)

    @property
    def request_successful(self):
        return self.is_element_displayed(*self._thank_you_locator)
