# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class FirefoxWhatsNewAfricaPage(BasePage):

    URL_TEMPLATE = '/{locale}/firefox/79.0/whatsnew/africa/'

    _qr_code_locator = (By.CSS_SELECTOR, '.lite-qrcode-container > img')

    @property
    def is_qr_code_displayed(self):
        return self.is_element_displayed(*self._qr_code_locator)
