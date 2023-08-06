# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class FirefoxWhatsNew115Page(BasePage):
    _URL_TEMPLATE = "/{locale}/firefox/115.0/whatsnew/"

    _qrcode_locator = (By.CSS_SELECTOR, ".c-qrcode svg")

    @property
    def is_qrcode_displayed(self):
        return self.is_element_displayed(*self._qrcode_locator)
