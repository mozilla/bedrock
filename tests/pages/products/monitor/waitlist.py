# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected

from pages.base import BasePage


class MonitorWaitlistPage(BasePage):
    _URL_TEMPLATE = "/{locale}/products/monitor/waitlist-{slug}/{params}"

    _newsletter_form_locator = (By.ID, "newsletter-form")
    _email_locator = (By.ID, "id_email")
    _form_details_locator = (By.ID, "newsletter-details")
    _privacy_policy_checkbox_locator = (By.ID, "privacy")
    _privacy_policy_link_locator = (By.CSS_SELECTOR, 'label[for="privacy"] a')
    _submit_button_locator = (By.ID, "newsletter-submit")
    _thank_you_locator = (By.ID, "newsletter-thanks")
    _error_list_locator = (By.ID, "newsletter-errors")
    _service_not_available_message_locator = (By.CLASS_NAME, "c-not-available")

    def expand_form(self):
        # scroll newsletter into view before expanding the form
        self.scroll_element_into_view(*self._newsletter_form_locator)
        assert not self.is_form_detail_displayed, "Form detail is already displayed"
        self.find_element(*self._email_locator).send_keys("")
        self.wait.until(expected.visibility_of_element_located(self._privacy_policy_checkbox_locator))

    @property
    def is_newsletter_form_displayed(self):
        return self.is_element_displayed(*self._newsletter_form_locator)

    @property
    def is_form_detail_displayed(self):
        return self.is_element_displayed(*self._form_details_locator)

    @property
    def email(self):
        return self.find_element(*self._email_locator).get_attribute("value")

    def type_email(self, value):
        self.find_element(*self._email_locator).send_keys(value)

    @property
    def privacy_policy_accepted(self):
        el = self.find_element(*self._privacy_policy_checkbox_locator)
        return el.is_selected()

    def accept_privacy_policy(self):
        el = self.find_element(*self._privacy_policy_checkbox_locator)
        assert not el.is_selected(), "Privacy policy has already been accepted"
        el.click()
        assert el.is_selected(), "Privacy policy has not been accepted"

    @property
    def is_form_success_displayed(self):
        return self.is_element_displayed(*self._thank_you_locator)

    @property
    def is_form_error_displayed(self):
        return self.is_element_displayed(*self._error_list_locator)

    @property
    def is_service_not_available_message_displayed(self):
        return self.is_element_displayed(*self._service_not_available_message_locator)

    def click_sign_up_now(self, expected_result=None):
        self.find_element(*self._submit_button_locator).click()
        if expected_result == "error":
            self.wait.until(expected.visibility_of_element_located(self._error_list_locator))
        else:
            self.wait.until(expected.visibility_of_element_located(self._thank_you_locator))
