# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class FirefoxWhatsNew111Page(BasePage):
    _URL_TEMPLATE = "/{locale}/firefox/111.0/whatsnew/"

    _translate_button_locator = (By.CSS_SELECTOR, ".wnp-main-cta.translate .mzp-c-button")
    _pdf_button_locator = (By.CSS_SELECTOR, ".wnp-main-cta.pdf .mzp-c-button")

    @property
    def is_translate_button_displayed(self):
        return self.is_element_displayed(*self._translate_button_locator)

    @property
    def is_pdf_button_displayed(self):
        return self.is_element_displayed(*self._pdf_button_locator)
