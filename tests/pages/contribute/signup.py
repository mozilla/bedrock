# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pages.contribute.base import ContributeBasePage


class ContributeSignUpPage(ContributeBasePage):

    _url = '{base_url}/{locale}/contribute/signup'

    _name_locator = (By.ID, 'id_name')
    _email_locator = (By.ID, 'id_email')
    _country_locator = (By.ID, 'id_country')
    _message_locator = (By.ID, 'person-message')
    _html_format_locator = (By.ID, 'id_format_0')
    _text_format_locator = (By.ID, 'id_format_1')
    _privacy_policy_checkbox_locator = (By.ID, 'id_privacy')
    _newsletter_checkbox_locator = (By.ID, 'id_newsletter')
    _submit_button_locator = (By.CSS_SELECTOR, '.submit > button')
    _success_url_slug = '/contribute/thankyou/'
    _areas_region_locator = (By.CLASS_NAME, 'areas')
    _coding_category_locator = (By.CLASS_NAME, 'category-coding')
    _coding_area_locator = (By.CSS_SELECTOR, '#area-coding select')
    _helping_category_locator = (By.CLASS_NAME, 'category-helping')

    def select_coding_category(self):
        self.find_element(self._coding_category_locator).click()
        self.wait.until(lambda s: self.is_coding_area_required)
        assert self.is_coding_area_displayed

    def select_helping_category(self):
        self.find_element(self._helping_category_locator).click()

    @property
    def is_coding_area_displayed(self):
        return self.is_element_displayed(self._coding_area_locator)

    @property
    def is_coding_area_required(self):
        el = self.find_element(self._coding_area_locator)
        return el.get_attribute('required') == 'true'

    def select_coding_area(self, value):
        el = self.find_element(self._coding_area_locator)
        Select(el).select_by_visible_text(value)

    @property
    def is_areas_region_displayed(self):
        return self.is_element_displayed(self._areas_region_locator)

    def type_name(self, value):
        self.find_element(self._name_locator).send_keys(value)

    def type_email(self, value):
        self.find_element(self._email_locator).send_keys(value)

    def select_country(self, value):
        el = self.find_element(self._country_locator)
        Select(el).select_by_visible_text(value)

    def select_html_format(self):
        self.find_element(self._html_format_locator).click()

    def select_text_format(self):
        self.find_element(self._text_format_locator).click()

    def accept_privacy_policy(self):
        el = self.find_element(self._privacy_policy_checkbox_locator)
        assert not el.is_selected(), 'Privacy policy has already been accepted'
        el.click()
        assert el.is_selected(), 'Privacy policy has not been accepted'

    def click_start_contributing(self):
        self.find_element(self._submit_button_locator).click()
        self.wait.until(lambda s: self.sign_up_successful)

    @property
    def sign_up_successful(self):
        return self._success_url_slug in self.selenium.current_url
