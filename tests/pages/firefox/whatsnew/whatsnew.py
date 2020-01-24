# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage
from pages.regions.send_to_device import SendToDevice


class FirefoxWhatsNewPage(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/whatsnew/all/'

    _qr_code_locator = (By.CSS_SELECTOR, '.qr-code img')
    _firefox_lite_qr_code_locator = (By.CSS_SELECTOR, '.lite-qrcode-container img')

    @property
    def send_to_device(self):
        return SendToDevice(self)

    @property
    def is_qr_code_displayed(self):
        return self.is_element_displayed(*self._qr_code_locator)

    @property
    def is_firefox_lite_qr_code_displayed(self):
        return self.is_element_displayed(*self._firefox_lite_qr_code_locator)
