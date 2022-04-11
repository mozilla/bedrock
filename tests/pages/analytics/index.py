# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By

from pages.base import BasePage


class AnalyticsTestPage(BasePage):

    _URL_TEMPLATE = "/{locale}/external/analytics"

    # GA buttons to test
    _ga_test_button_download_locator = (By.CSS_SELECTOR, ".mzp-c-button[data-link-type=download-test]")

    _ga_test_button_link_locator = (By.CSS_SELECTOR, ".mzp-c-button[data-cta-type=button-test]")

    _ga_test_button_account_link_locator = (By.CSS_SELECTOR, ".mzp-c-button[data-cta-type=fxa-sync-test]")

    @property
    def download_button_is_displayed(self):
        return self.is_element_displayed(*self._ga_test_button_download_locator)

    @property
    def download_button(self):
        return self.find_element(*self._ga_test_button_download_locator)

    @property
    def link_button_is_displayed(self):
        return self.is_element_displayed(*self._ga_test_button_link_locator)

    @property
    def link_button(self):
        return self.find_element(*self._ga_test_button_link_locator)

    @property
    def account_button_is_displayed(self):
        return self.is_element_displayed(*self._ga_test_button_account_link_locator)

    @property
    def account_button(self):
        return self.find_element(*self._ga_test_button_account_link_locator)

    def click_download_button(self):
        return self.find_element(*self._ga_test_button_download_locator).click()

    def click_link_button(self):
        return self.find_element(*self._ga_test_button_link_locator).click()

    def click_account_button(self):
        return self.find_element(*self._ga_test_button_account_link_locator).click()
