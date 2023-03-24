# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected

from pages.base import BasePage


class FirefoxWhatsNew112Page(BasePage):
    _URL_TEMPLATE = "/{locale}/firefox/112.0/whatsnew/"

    _set_default_button_locator = (By.CSS_SELECTOR, ".wnp-cta-default .mzp-c-button")
    _protection_report_button_locator = (By.CSS_SELECTOR, ".wnp-cta-protections .mzp-c-button")

    def wait_for_page_to_load(self):
        self.wait.until(lambda s: self.seed_url in s.current_url)
        el = self.find_element(By.TAG_NAME, "html")
        self.wait.until(lambda s: "loaded" in el.get_attribute("class"))
        self.wait.until(expected.visibility_of_element_located(self._set_default_button_locator))
        return self

    @property
    def is_firefox_set_default_button_displayed(self):
        return self.is_element_displayed(*self._set_default_button_locator)

    @property
    def is_firefox_protection_report_button_displayed(self):
        return self.is_element_displayed(*self._protection_report_button_locator)
