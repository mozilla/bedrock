# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage


class FirefoxWelcomePage3(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/welcome/3/'

    _fxa_primary_button_locator = (By.CSS_SELECTOR, '.primary-cta .js-fxa-product-button')
    _fxa_secondary_button_locator = (By.CSS_SELECTOR, '.secondary-cta .js-fxa-product-button')

    @property
    def is_primary_fxa_button_displayed(self):
        return self.is_element_displayed(*self._fxa_primary_button_locator)

    @property
    def is_secondary_fxa_button_displayed(self):
        return self.is_element_displayed(*self._fxa_secondary_button_locator)
