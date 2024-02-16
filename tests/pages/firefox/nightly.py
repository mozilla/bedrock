# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class FirstRunPage(BasePage):
    _URL_TEMPLATE = "/{locale}/firefox/nightly/firstrun/"

    _start_testing_locator = (By.CSS_SELECTOR, ".contribute .test .mzp-c-button")
    _start_coding_locator = (By.CSS_SELECTOR, ".contribute .code .mzp-c-button")
    _start_localizing_locator = (By.CSS_SELECTOR, ".contribute .localize .mzp-c-button")

    @property
    def is_start_testing_displayed(self):
        return self.is_element_displayed(*self._start_testing_locator)

    @property
    def is_start_coding_displayed(self):
        return self.is_element_displayed(*self._start_coding_locator)

    @property
    def is_start_localizing_displayed(self):
        return self.is_element_displayed(*self._start_localizing_locator)
