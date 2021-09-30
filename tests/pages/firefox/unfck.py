# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.regions.download_button import DownloadButton


class FirefoxUnfckPage(BasePage):

    _URL_TEMPLATE = "/{locale}/firefox/unfck/"

    _download_button_locator = (By.ID, "download-button-desktop-release")
    _send_to_mobile_button_locator = (By.CSS_SELECTOR, ".mzp-c-hero .cc-send-to-mobile .mzp-c-button")
    _thank_you_message_locator = (By.CSS_SELECTOR, ".mzp-c-hero.mzp-t-firefox.show-firefox")

    @property
    def download_button(self):
        el = self.find_element(*self._download_button_locator)
        return DownloadButton(self, root=el)

    @property
    def is_send_to_mobile_button_displayed(self):
        return self.is_element_displayed(*self._send_to_mobile_button_locator)

    @property
    def is_thank_you_message_displayed(self):
        return self.is_element_displayed(*self._thank_you_message_locator)
