# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class FirefoxWhatsNew96Page(BasePage):

    _URL_TEMPLATE = "/{locale}/firefox/96.0/whatsnew/{params}"

    _relay_button_signed_in_locator = (By.CSS_SELECTOR, ".show-fxa-supported-signed-in .wnp-main-cta .mzp-c-button")
    _fxa_button_signed_out_locator = (By.CSS_SELECTOR, ".show-fxa-supported-signed-out .wnp-main-cta .mzp-c-button")

    def wait_for_page_to_load(self):
        self.wait.until(lambda s: self.seed_url in s.current_url)
        el = self.find_element(By.TAG_NAME, "body")
        self.wait.until(lambda s: "state-fxa-default" not in el.get_attribute("class"))
        return self

    @property
    def is_relay_button_displayed_when_signed_in(self):
        return self.is_element_displayed(*self._relay_button_signed_in_locator)

    @property
    def is_fxa_button_displayed_when_signed_out(self):
        return self.is_element_displayed(*self._fxa_button_signed_out_locator)
