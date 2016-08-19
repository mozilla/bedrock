# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.select import Select

from pages.base import BasePage


class NewsletterBasePage(BasePage):

    URL_TEMPLATE = '/{locale}/newsletter/'

    _email_locator = (By.ID, 'id_email')
    _country_locator = (By.ID, 'id_country')
    _language_locator = (By.ID, 'id_lang')
    _html_format_locator = (By.ID, 'id_fmt_0')
    _text_format_locator = (By.ID, 'id_fmt_1')
    _privacy_policy_checkbox_locator = (By.ID, 'id_privacy')
    _privacy_policy_link_locator = (By.CSS_SELECTOR, 'label[for="id_privacy"] a')
    _submit_button_locator = (By.ID, 'footer_email_submit')
    _thank_you_locator = (By.CSS_SELECTOR, '#newsletter-form-thankyou h3')

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
        return Select(el).first_selected_option.text

    def select_language(self, value):
        el = self.find_element(*self._language_locator)
        Select(el).select_by_visible_text(value)

    @property
    def html_format_selected(self):
        return self.find_element(*self._html_format_locator).is_selected()

    def select_html_format(self):
        self.find_element(*self._html_format_locator).click()

    @property
    def text_format_selected(self):
        return self.find_element(*self._text_format_locator).is_selected()

    def select_text_format(self):
        self.find_element(*self._text_format_locator).click()

    @property
    def privacy_policy_accepted(self):
        el = self.find_element(*self._privacy_policy_checkbox_locator)
        return el.is_selected()

    def accept_privacy_policy(self):
        el = self.find_element(*self._privacy_policy_checkbox_locator)
        assert not el.is_selected(), 'Privacy policy has already been accepted'
        el.click()
        assert el.is_selected(), 'Privacy policy has not been accepted'

    @property
    def is_privacy_policy_link_displayed(self):
        return self.is_element_displayed(*self._privacy_policy_link_locator)

    def click_sign_me_up(self):
        self.find_element(*self._submit_button_locator).click()
        self.wait.until(expected.visibility_of_element_located(self._thank_you_locator))

    @property
    def sign_up_successful(self):
        return self.is_element_displayed(*self._thank_you_locator)
