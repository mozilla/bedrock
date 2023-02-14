# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.regions.join_firefox_form import JoinFirefoxForm


class FirefoxProductsPage(BasePage):
    _URL_TEMPLATE = "/{locale}/firefox/products/"

    _monitor_button_locator = (By.CSS_SELECTOR, "#qa-monitor-button-wrapper a.js-fxa-product-button")

    @property
    def is_monitor_button_displayed(self):
        return self.is_element_displayed(*self._monitor_button_locator)

    @property
    def join_firefox_form(self):
        return JoinFirefoxForm(self)
