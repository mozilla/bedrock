# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class FirefoxWhatsNew103Page(BasePage):

    _URL_TEMPLATE = "/{locale}/firefox/103.0/whatsnew/{params}"

    _firefox_default_button_locator = (By.CSS_SELECTOR, ".wnp-main-cta .mzp-c-button")
    _default_success_message_locator = (By.CLASS_NAME, "wnp-alt-msg")

    @property
    def is_firefox_default_button_displayed(self):
        return self.is_element_displayed(*self._firefox_default_button_locator)

    @property
    def is_firefox_default_success_message_displayed(self):
        return self.is_element_displayed(*self._default_success_message_locator)
