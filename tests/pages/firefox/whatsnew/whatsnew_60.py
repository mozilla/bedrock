# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage


class FirefoxWhatsNew60Page(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/60.0/whatsnew/all/{params}'

    _account_button_locator = (By.CSS_SELECTOR, '.content-main .js-fxa-product-button')

    @property
    def is_account_button_displayed(self):
        return self.is_element_displayed(*self._account_button_locator)
