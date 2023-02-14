# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.regions.send_to_device import SendToDevice


class FirefoxWhatsNew60Page(BasePage):
    _URL_TEMPLATE = "/{locale}/firefox/60.0/whatsnew/{params}"

    _account_button_locator = (By.CSS_SELECTOR, ".wnp-content-main .js-fxa-product-button")
    _qr_code_locator = (By.CSS_SELECTOR, "#qr-wrapper img")

    def wait_for_page_to_load(self):
        self.wait.until(lambda s: self.seed_url in s.current_url)
        el = self.find_element(By.TAG_NAME, "body")
        self.wait.until(lambda s: "state-fxa-default" not in el.get_attribute("class"))
        return self

    @property
    def is_account_button_displayed(self):
        return self.is_element_displayed(*self._account_button_locator)

    @property
    def send_to_device(self):
        return SendToDevice(self)

    @property
    def is_qr_code_displayed(self):
        return self.is_element_displayed(*self._qr_code_locator)
