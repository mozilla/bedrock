# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.select import Select


class FirefoxWhatsNew87Page(BasePage):

    _URL_TEMPLATE = '/{locale}/firefox/87.0/whatsnew/all/'

    _email_locator = (By.ID, 'id_email')
    _country_locator = (By.ID, 'id_country')
    _language_locator = (By.ID, 'id_lang')
    _submit_button_locator = (By.ID, 'newsletter-submit')
    _thank_you_locator = (By.ID, 'newsletter-thanks')
    _error_list_locator = (By.ID, 'newsletter-errors')

    @property
    def email(self):
        return self.find_element(*self._email_locator).get_attribute('value')

    def type_email(self, value):
        self.find_element(*self._email_locator).send_keys(value)

    @property
    def country(self):
        el = self.find_element(*self._country_locator)
        return el.find_element(By.CSS_SELECTOR, 'option[selected]').text

    def select_country(self, value):
        el = self.find_element(*self._country_locator)
        Select(el).select_by_visible_text(value)

    @property
    def language(self):
        el = self.find_element(*self._language_locator)
        return el.find_element(By.CSS_SELECTOR, 'option[selected]').text

    def select_language(self, value):
        el = self.find_element(*self._language_locator)
        Select(el).select_by_visible_text(value)

    @property
    def is_form_success_displayed(self):
        return self.is_element_displayed(*self._thank_you_locator)

    @property
    def is_form_error_displayed(self):
        return self.is_element_displayed(*self._error_list_locator)

    def click_sign_me_up(self, expected_result=None):
        self.find_element(*self._submit_button_locator).click()
        if expected_result == 'error':
            self.wait.until(expected.visibility_of_element_located(self._error_list_locator))
        else:
            self.wait.until(expected.visibility_of_element_located(self._thank_you_locator))
