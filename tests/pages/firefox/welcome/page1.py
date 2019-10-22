# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage


class FirefoxWelcomePage1(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/welcome/1/'

    _monitor_primary_button_locator = (By.CSS_SELECTOR, '.primary-cta .js-monitor-button')
    _monitor_secondary_button_locator = (By.CSS_SELECTOR, '.secondary-cta .js-monitor-button')

    @property
    def is_primary_monitor_button_displayed(self):
        return self.is_element_displayed(*self._monitor_primary_button_locator)

    @property
    def is_secondary_monitor_button_displayed(self):
        return self.is_element_displayed(*self._monitor_secondary_button_locator)
