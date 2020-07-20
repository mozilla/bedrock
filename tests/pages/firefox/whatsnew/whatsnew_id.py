# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class FirefoxWhatsNewIDPage(BasePage):

    URL_TEMPLATE = '/id/firefox/79.0/whatsnew/all/'

    _firefox_lite_qr_code_locator = (By.CSS_SELECTOR, '.lite-qrcode-container img')

    @property
    def is_firefox_lite_qr_code_displayed(self):
        return self.is_element_displayed(*self._firefox_lite_qr_code_locator)
