# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class FirefoxWhatsNew123Page(BasePage):
    _URL_TEMPLATE = "/{locale}/firefox/123.0/whatsnew/"

    _try_reader_view_button_locator = (By.CSS_SELECTOR, ".wnp-main-cta.try-reader-view .mzp-c-button")

    @property
    def is_try_reader_view_button_displayed(self):
        return self.is_element_displayed(*self._try_reader_view_button_locator)
