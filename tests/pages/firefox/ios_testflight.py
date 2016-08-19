# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected

from pages.firefox.base import FirefoxBasePage


class iOSTestFlightPage(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/ios/testflight/'

    _email_locator = (By.ID, 'id_email')
    _html_format_locator = (By.ID, 'id_fmt_0')
    _privacy_policy_checkbox_locator = (By.ID, 'id_privacy')
    _privacy_policy_link_locator = (By.CSS_SELECTOR, 'label[for="id_privacy"] span a')
    _submit_button_locator = (By.ID, 'footer_email_submit')
    _terms_checkbox_locator = (By.ID, 'id_terms')
    _terms_link_locator = (By.CSS_SELECTOR, 'label[for="id_terms"] span a')
    _text_format_locator = (By.ID, 'id_fmt_1')
    _thank_you_locator = (By.CSS_SELECTOR, '#newsletter-form-thankyou h2')

    @property
    def email(self):
        return self.find_element(*self._email_locator).get_attribute('value')

    @property
    def html_format_selected(self):
        return self.find_element(*self._html_format_locator).is_selected()

    @property
    def is_privacy_policy_link_displayed(self):
        return self.is_element_displayed(*self._privacy_policy_link_locator)

    @property
    def is_terms_link_displayed(self):
        return self.is_element_displayed(*self._terms_link_locator)

    @property
    def privacy_policy_accepted(self):
        el = self.find_element(*self._privacy_policy_checkbox_locator)
        return el.is_selected()

    @property
    def terms_accepted(self):
        el = self.find_element(*self._terms_checkbox_locator)
        return el.is_selected()

    @property
    def sign_up_successful(self):
        return self.is_element_displayed(*self._thank_you_locator)

    @property
    def text_format_selected(self):
        return self.find_element(*self._text_format_locator).is_selected()

    def accept_privacy_policy(self):
        el = self.find_element(*self._privacy_policy_checkbox_locator)
        assert not el.is_selected(), 'Privacy policy has already been accepted'
        el.click()
        assert el.is_selected(), 'Privacy policy has not been accepted'

    def accept_terms(self):
        el = self.find_element(*self._terms_checkbox_locator)
        assert not el.is_selected(), 'Terms have already been accepted'
        el.click()
        assert el.is_selected(), 'Terms have not been accepted'

    def click_sign_me_up(self):
        self.find_element(*self._submit_button_locator).click()
        self.wait.until(expected.visibility_of_element_located(self._thank_you_locator))

    def select_text_format(self):
        self.find_element(*self._text_format_locator).click()

    def type_email(self, value):
        self.find_element(*self._email_locator).send_keys(value)
