# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class FirefoxWhatsNew89Page(BasePage):

    _URL_TEMPLATE = '/{locale}/firefox/89.0/whatsnew/all/'

    _vpn_button_locator = (By.CSS_SELECTOR, '.wnp-content-main .mzp-c-button')

    @property
    def is_vpn_button_displayed(self):
        return self.is_element_displayed(*self._vpn_button_locator)
