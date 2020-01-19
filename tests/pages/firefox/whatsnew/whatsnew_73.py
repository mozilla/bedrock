# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage
from pages.regions.modal import ModalProtocol
from pages.regions.send_to_device import SendToDevice


class FirefoxWhatsNew73Page(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/73.0/whatsnew/all/{params}'

    _set_default_button_locator = (By.CSS_SELECTOR, '.content-main .js-fxa-product-button')
    _mobile_button_locator = (By.CSS_SELECTOR, '.js-modal-link')
    _firefox_qr_code_locator = (By.CSS_SELECTOR, '.mzp-c-modal .qr-code-wrapper .firefox-qr')

    @property
    def send_to_device(self):
        return SendToDevice(self)

    @property
    def is_mobile_qr_code_displayed(self):
        return self.is_element_displayed(*self._firefox_qr_code_locator)

    def open_modal(self, locator):
        modal = ModalProtocol(self)
        self.find_element(*locator).click()
        self.wait.until(lambda s: modal.is_displayed)
        return modal

    def click_get_mobile_button(self):
        self.scroll_element_into_view(*self._mobile_button_locator)
        return self.open_modal(self._mobile_button_locator)
