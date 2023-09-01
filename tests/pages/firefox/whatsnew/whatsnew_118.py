# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from time import sleep

from selenium.webdriver.common.by import By

from pages.base import BasePage


class FirefoxWhatsNew118Page(BasePage):
    _URL_TEMPLATE = "/{locale}/firefox/118.0/whatsnew/"

    # EU pages
    _set_alt_cta_button_locator = (By.CSS_SELECTOR, "#cta-try .mzp-c-button")
    # NA pages
    _set_try_it_button_locator = (By.ID, "cta-now")

    def wait_for_page_to_load(self):
        self.wait.until(lambda s: self.seed_url in s.current_url)
        el = self.find_element(By.TAG_NAME, "html")
        self.wait.until(lambda s: "loaded" in el.get_attribute("class"))
        # EU pages UI Tour call will time out at 1 second, NA pages don't have UI Tour call
        sleep(1.2)
        return self

    @property
    def is_firefox_alt_cta_button_displayed(self):
        return self.is_element_displayed(*self._set_alt_cta_button_locator)

    @property
    def is_try_it_button_displayed(self):
        return self.is_element_displayed(*self._set_try_it_button_locator)
