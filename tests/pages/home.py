# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class HomePage(BasePage):

    _privacy_hero_button_locator = (By.CSS_SELECTOR, '.privacy-promise-hero .mzp-c-button')
    _rest_of_world_download_button_locator = (By.ID, 'download-intro')  # legacy home page
    _primary_download_button_locator = (By.ID, 'download-primary')
    _secondary_download_button_locator = (By.ID, 'download-secondary')
    _primary_accounts_button_locator = (By.ID, 'fxa-learn-primary')
    _secondary_accounts_button_locator = (By.ID, 'fxa-learn-secondary')

    @property
    def is_privacy_hero_button_displayed(self):
        return self.is_element_displayed(*self._privacy_hero_button_locator)

    @property
    def is_rest_of_world_download_button_displayed(self):
        return self.is_element_displayed(*self._rest_of_world_download_button_locator)

    @property
    def is_primary_download_button_displayed(self):
        return self.is_element_displayed(*self._primary_download_button_locator)

    @property
    def is_secondary_download_button_displayed(self):
        return self.is_element_displayed(*self._secondary_download_button_locator)

    @property
    def is_primary_accounts_button_displayed(self):
        return self.is_element_displayed(*self._primary_accounts_button_locator)

    @property
    def is_secondary_accounts_button_displayed(self):
        return self.is_element_displayed(*self._secondary_accounts_button_locator)
