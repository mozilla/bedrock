# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class FirefoxWhatsNewNightly70Page(BasePage):
    _URL_TEMPLATE = "/{locale}/firefox/70.0a1/whatsnew/"

    _upgrade_message_locator = (By.CSS_SELECTOR, ".content-wrapper .c-emphasis-box-title")

    @property
    def is_upgrade_message_displayed(self):
        return self.is_element_displayed(*self._upgrade_message_locator)
