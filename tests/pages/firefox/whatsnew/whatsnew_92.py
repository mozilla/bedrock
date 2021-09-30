# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class FirefoxWhatsNew92Page(BasePage):

    _URL_TEMPLATE = "/{locale}/firefox/92.0/whatsnew/all/"

    _pocket_primary_button_locator = (By.CSS_SELECTOR, ".wnp-main-cta .mzp-c-button")
    _pocket_secondary_button_locator = (By.CSS_SELECTOR, ".wnp-footer-cta .mzp-c-button")

    @property
    def is_pocket_primary_button_displayed(self):
        return self.is_element_displayed(*self._pocket_primary_button_locator)

    @property
    def is_pocket_secondary_button_displayed(self):
        return self.is_element_displayed(*self._pocket_secondary_button_locator)
