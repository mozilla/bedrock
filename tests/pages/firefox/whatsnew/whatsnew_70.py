# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage


class FirefoxWhatsNew70Page(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/70.0/whatsnew/all/{params}'

    _signed_out_monitor_button_locator = (By.CSS_SELECTOR, '.show-fxa-supported-signed-out .js-fxa-product-button')
    _signed_in_monitor_button_locator = (By.CSS_SELECTOR, '.show-fxa-supported-signed-in .js-fxa-product-button')

    def wait_for_page_to_load(self):
        self.wait.until(lambda s: self.seed_url in s.current_url)
        el = self.find_element(By.TAG_NAME, 'body')
        self.wait.until(lambda s: 'state-fxa-default' not in el.get_attribute('class'))
        return self

    @property
    def is_signed_out_monitor_button_displayed(self):
        return self.is_element_displayed(*self._signed_out_monitor_button_locator)

    @property
    def is_signed_in_monitor_button_displayed(self):
        return self.is_element_displayed(*self._signed_in_monitor_button_locator)
