# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class FirefoxWhatsNew71Page(BasePage):

    URL_TEMPLATE = '/{locale}/firefox/71.0/whatsnew/all/{params}'

    _primary_account_button_locator = (By.CSS_SELECTOR, '.content-main .js-fxa-product-button')
    _secondary_account_button_locator = (By.CSS_SELECTOR, '.content-extra .js-fxa-product-button')

    @property
    def is_primary_account_button_displayed(self):
        return self.is_element_displayed(*self._primary_account_button_locator)

    @property
    def is_secondary_account_button_displayed(self):
        return self.is_element_displayed(*self._secondary_account_button_locator)
