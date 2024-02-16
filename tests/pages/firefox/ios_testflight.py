# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected

from pages.base import BasePage


class iOSTestFlightPage(BasePage):
    _URL_TEMPLATE = "/{locale}/firefox/ios/testflight/"

    _email_locator = (By.ID, "id_email")
    _html_format_locator = (By.ID, "format-html")
    _privacy_policy_checkbox_locator = (By.ID, "id_privacy")
    _privacy_policy_link_locator = (By.CSS_SELECTOR, 'label[for="id_privacy"] a')
    _submit_button_locator = (By.ID, "newsletter-submit")
    _terms_checkbox_locator = (By.ID, "id_terms")
    _terms_link_locator = (By.CSS_SELECTOR, 'label[for="id_terms"] a')
    _text_format_locator = (By.ID, "format-text")
    _thank_you_locator = (By.ID, "newsletter-thanks")
    _form_details_locator = (By.ID, "newsletter-details")
    _error_list_locator = (By.ID, "newsletter-errors")

    @property
    def is_form_error_displayed(self):
        return self.is_element_displayed(*self._error_list_locator)

    @property
    def email(self):
        return self.find_element(*self._email_locator).get_attribute("value")

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
        assert not el.is_selected(), "Privacy policy has already been accepted"
        el.click()
        assert el.is_selected(), "Privacy policy has not been accepted"

    def accept_terms(self):
        el = self.find_element(*self._terms_checkbox_locator)
        assert not el.is_selected(), "Terms have already been accepted"
        el.click()
        assert el.is_selected(), "Terms have not been accepted"

    def click_sign_me_up(self, expected_result=None):
        self.find_element(*self._submit_button_locator).click()
        if expected_result == "error":
            self.wait.until(expected.visibility_of_element_located(self._error_list_locator))
        else:
            self.wait.until(expected.visibility_of_element_located(self._thank_you_locator))

    def select_text_format(self):
        self.find_element(*self._text_format_locator).click()

    def type_email(self, value):
        self.find_element(*self._email_locator).send_keys(value)

    def expand_form(self):
        # scroll newsletter into view before expanding the form
        self.scroll_element_into_view(*self._email_locator)
        assert not self.is_form_detail_displayed, "Form detail is already displayed"
        self.find_element(*self._email_locator).send_keys("")
        self.wait.until(expected.visibility_of_element_located(self._privacy_policy_checkbox_locator))

    @property
    def is_form_detail_displayed(self):
        return self.is_element_displayed(*self._form_details_locator)
