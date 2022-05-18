# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class VPNDownloadPage(BasePage):

    _URL_TEMPLATE = "/{locale}/products/vpn/download/{params}"

    _windows_download_button_locator = (By.CSS_SELECTOR, ".mzp-c-button[data-cta-text='VPN Download (Windows)']")
    _mac_download_button_locator = (By.CSS_SELECTOR, ".mzp-c-button[data-cta-text='VPN Download (macOS)']")
    _linux_download_button_locator = (By.CSS_SELECTOR, ".mzp-c-button[data-cta-text='VPN Download (Linux)']")
    _android_download_button_locator = (By.CSS_SELECTOR, ".mzp-c-button[data-cta-text='VPN Download (Android)']")
    _ios_download_button_locator = (By.CSS_SELECTOR, ".mzp-c-button[data-cta-text='VPN Download (iOS)']")

    @property
    def is_windows_download_button_displayed(self):
        return self.is_element_displayed(*self._windows_download_button_locator)

    @property
    def is_mac_download_button_displayed(self):
        return self.is_element_displayed(*self._mac_download_button_locator)

    @property
    def is_linux_download_button_displayed(self):
        return self.is_element_displayed(*self._linux_download_button_locator)

    @property
    def is_android_download_button_displayed(self):
        return self.is_element_displayed(*self._android_download_button_locator)

    @property
    def is_ios_download_button_displayed(self):
        return self.is_element_displayed(*self._ios_download_button_locator)
