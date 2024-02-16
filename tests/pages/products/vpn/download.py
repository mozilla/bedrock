# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class VPNDownloadPage(BasePage):
    _URL_TEMPLATE = "/{locale}/products/vpn/download/{params}"

    _download_container_locator = (By.CSS_SELECTOR, ".vpn-download-options")
    _windows_download_button_locator = (By.CSS_SELECTOR, "a[data-cta-text='VPN Download (Windows)']")
    _mac_download_button_locator = (By.CSS_SELECTOR, "a[data-cta-text='VPN Download (macOS)']")
    _linux_download_button_locator = (By.CSS_SELECTOR, "a[data-cta-text='VPN Download (Linux)']")
    _android_download_button_locator = (By.CSS_SELECTOR, "a[data-cta-text='VPN Download (Android)']")
    _ios_download_button_locator = (By.CSS_SELECTOR, "a[data-cta-text='VPN Download (iOS)']")

    @property
    def windows_download_button(self):
        els = [el for el in self.find_elements(*self._windows_download_button_locator) if el.is_displayed()]
        assert len(els) == 1, "Expected one Windows download link to be displayed"
        return els[0]

    @property
    def mac_download_button(self):
        els = [el for el in self.find_elements(*self._mac_download_button_locator) if el.is_displayed()]
        assert len(els) == 1, "Expected one macOS download link to be displayed"
        return els[0]

    @property
    def linux_download_button(self):
        els = [el for el in self.find_elements(*self._linux_download_button_locator) if el.is_displayed()]
        assert len(els) == 1, "Expected one Linux download link to be displayed"
        return els[0]

    @property
    def android_download_button(self):
        els = [el for el in self.find_elements(*self._android_download_button_locator) if el.is_displayed()]
        assert len(els) == 1, "Expected one Android download link to be displayed"
        return els[0]

    @property
    def ios_download_button(self):
        els = [el for el in self.find_elements(*self._ios_download_button_locator) if el.is_displayed()]
        assert len(els) == 1, "Expected one iOS download link to be displayed"
        return els[0]

    @property
    def is_windows_download_button_displayed(self):
        return self.windows_download_button.is_displayed()

    @property
    def is_mac_download_button_displayed(self):
        return self.mac_download_button.is_displayed()

    @property
    def is_linux_download_button_displayed(self):
        return self.linux_download_button.is_displayed()

    @property
    def is_android_download_button_displayed(self):
        return self.android_download_button.is_displayed()

    @property
    def is_ios_download_button_displayed(self):
        return self.ios_download_button.is_displayed()

    @property
    def is_download_container_displayed(self):
        return self.is_element_displayed(*self._download_container_locator)
