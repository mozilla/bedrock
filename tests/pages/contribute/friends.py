# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.select import Select

from pages.contribute.base import ContributeBasePage


class ContributeFriendsPage(ContributeBasePage):

    URL_TEMPLATE = '/{locale}/contribute/friends/'

    _email_locator = (By.ID, 'id_email')
    _fx_and_you_locator = (By.ID, 'id_fx-and-you')
    _country_locator = (By.ID, 'id_country')
    _html_format_locator = (By.ID, 'id_fmt_0')
    _newsletters_locator = (By.ID, 'id_newsletters')
    _privacy_policy_checkbox_locator = (By.ID, 'id_privacy')
    _privacy_policy_link_locator = (By.CSS_SELECTOR, 'label[for="id_privacy"] span a')
    _signup_form_locator = (By.ID, 'newsletter-form')
    _submit_button_locator = (By.ID, 'footer_email_submit')
    _text_format_locator = (By.ID, 'id_fmt_1')
    _thank_you_locator = (By.CSS_SELECTOR, '#newsletter-form-thankyou h3')

    @property
    def email(self):
        return self.find_element(*self._email_locator).get_attribute('value')

    @property
    def country(self):
        el = self.find_element(*self._country_locator)
        return el.find_element(By.CSS_SELECTOR, 'option[selected]').text

    @property
    def html_format_selected(self):
        return self.find_element(*self._html_format_locator).is_selected()

    @property
    def is_signup_form_displayed(self):
        return self.is_element_displayed(*self._signup_form_locator)

    @property
    def is_privacy_policy_link_displayed(self):
        return self.is_element_displayed(*self._privacy_policy_link_locator)

    @property
    def newsletters(self):
        return self.find_element(*self._newsletters_locator).get_attribute('value')

    @property
    def privacy_policy_accepted(self):
        el = self.find_element(*self._privacy_policy_checkbox_locator)
        return el.is_selected()

    @property
    def sign_up_successful(self):
        return self.is_element_displayed(*self._thank_you_locator)

    @property
    def text_format_selected(self):
        return self.find_element(*self._text_format_locator).is_selected()

    def accept_fx_and_you(self):
        el = self.find_element(*self._fx_and_you_locator)
        assert not el.is_selected(), 'Firefox and you has already been accepted'
        el.click()
        assert el.is_selected(), 'Firefox and you has not been accepted'

    def accept_privacy_policy(self):
        el = self.find_element(*self._privacy_policy_checkbox_locator)
        assert not el.is_selected(), 'Privacy policy has already been accepted'
        el.click()
        assert el.is_selected(), 'Privacy policy has not been accepted'

    def click_sign_me_up(self):
        self.find_element(*self._submit_button_locator).click()
        self.wait.until(expected.visibility_of_element_located(self._thank_you_locator))

    def select_country(self, value):
        el = self.find_element(*self._country_locator)
        Select(el).select_by_visible_text(value)

    def select_text_format(self):
        self.find_element(*self._text_format_locator).click()

    def type_email(self, value):
        self.find_element(*self._email_locator).send_keys(value)
