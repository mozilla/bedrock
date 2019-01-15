# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage
from pages.regions.send_yourself import SendYourself


class FirefoxWhatsNewPage(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/whatsnew/'

    _qr_code_locator = (By.CSS_SELECTOR, '.qr-code img')
    _zh_tw_qr_code_locator = (By.CSS_SELECTOR, 'img.qrcode')

    @property
    def send_yourself(self):
        return SendYourself(self)
