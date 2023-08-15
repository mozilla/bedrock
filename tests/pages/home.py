# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class HomePage(BasePage):
    _URL_TEMPLATE = "/{locale}/"

    _firefox_download_button_locator = (By.ID, "homepage-get-firefox")
    _pocket_download_button_locator = (By.ID, "homepage-get-pocket")
    _relay_download_button_locator = (By.ID, "homepage-get-relay")
    _mozilla_vpn_download_button_locator = (By.ID, "homepage-get-mozilla-vpn")

    @property
    def is_firefox_download_button_displayed(self):
        return self.is_element_displayed(*self._firefox_download_button_locator)

    @property
    def is_pocket_download_button_displayed(self):
        return self.is_element_displayed(*self._pocket_download_button_locator)

    @property
    def is_relay_download_button_displayed(self):
        return self.is_element_displayed(*self._relay_download_button_locator)

    @property
    def is_mozilla_vpn_download_button_displayed(self):
        return self.is_element_displayed(*self._mozilla_vpn_download_button_locator)
