# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.regions.join_firefox_form import JoinFirefoxForm


class FirefoxAccountsPage(BasePage):
    _URL_TEMPLATE = "/{locale}/firefox/accounts/{params}"

    _firefox_monitor_button_locator = (By.CSS_SELECTOR, ".c-accounts-hero-body-signed-in .js-fxa-product-button")

    def wait_for_page_to_load(self):
        self.wait.until(lambda s: self.seed_url in s.current_url)
        el = self.find_element(By.TAG_NAME, "body")
        self.wait.until(lambda s: "state-fxa-default" not in el.get_attribute("class"))
        return self

    @property
    def join_firefox_form(self):
        return JoinFirefoxForm(self)

    @property
    def is_firefox_monitor_button_displayed(self):
        return self.is_element_displayed(*self._firefox_monitor_button_locator)
