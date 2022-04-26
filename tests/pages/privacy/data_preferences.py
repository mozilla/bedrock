# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class DataPreferencesPage(BasePage):

    _URL_TEMPLATE = "/{locale}/privacy/websites/data-preferences/"

    _preference_status_locator = (By.CSS_SELECTOR, ".data-preference-status")
    _opt_out_button_locator = (By.CLASS_NAME, "js-opt-out-button")
    _opt_in_button_locator = (By.CLASS_NAME, "js-opt-in-button")

    @property
    def is_opt_out_status_shown(self):
        return "is-opted-out" in self.find_element(*self._preference_status_locator).get_attribute("class")

    @property
    def is_opt_in_status_shown(self):
        return "is-opted-in" in self.find_element(*self._preference_status_locator).get_attribute("class")

    def click_opt_out(self):
        self.find_element(*self._opt_out_button_locator).click()

    def click_opt_in(self):
        self.find_element(*self._opt_in_button_locator).click()
