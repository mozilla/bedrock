# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.regions.modal import ModalProtocol
from pages.regions.send_to_device import SendToDevice


class FirefoxWelcomePage5(BasePage):

    _URL_TEMPLATE = "/{locale}/firefox/welcome/5/"

    _modal_primary_button_locator = (By.CSS_SELECTOR, ".primary-cta .js-modal-link")
    _modal_secondary_button_locator = (By.CSS_SELECTOR, ".secondary-cta .js-modal-link")
    _lockwise_qr_code_locator = (By.ID, "lockwise-qr")

    @property
    def send_to_device(self):
        return SendToDevice(self)

    @property
    def is_lockwise_qr_code_displayed(self):
        return self.is_element_displayed(*self._lockwise_qr_code_locator)

    @property
    def is_primary_modal_button_displayed(self):
        return self.is_element_displayed(*self._modal_primary_button_locator)

    @property
    def is_secondary_modal_button_displayed(self):
        return self.is_element_displayed(*self._modal_secondary_button_locator)

    def open_modal(self, locator):
        modal = ModalProtocol(self)
        self.find_element(*locator).click()
        self.wait.until(lambda s: modal.is_displayed)
        return modal

    def click_primary_modal_button(self):
        self.scroll_element_into_view(*self._modal_primary_button_locator)
        return self.open_modal(self._modal_primary_button_locator)
