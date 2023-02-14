# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class HomePage(BasePage):
    _URL_TEMPLATE = "/{locale}/"

    _primary_download_button_locator = (By.CSS_SELECTOR, "#download-primary > .download-link")
    _secondary_download_button_locator = (By.CSS_SELECTOR, "#download-secondary > .download-link")
    _primary_accounts_button_locator = (By.ID, "fxa-learn-primary")
    _secondary_accounts_button_locator = (By.ID, "fxa-learn-secondary")

    @property
    def is_primary_download_button_displayed(self):
        return self.is_element_displayed(*self._primary_download_button_locator)

    @property
    def is_primary_accounts_button_displayed(self):
        return self.is_element_displayed(*self._primary_accounts_button_locator)

    @property
    def is_secondary_download_button_displayed(self):
        return self.is_element_displayed(*self._secondary_download_button_locator)

    @property
    def is_secondary_accounts_button_displayed(self):
        return self.is_element_displayed(*self._secondary_accounts_button_locator)
