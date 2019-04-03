# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage
from pages.regions.modal import Modal
from pages.regions.send_to_device import SendToDevice


class FirefoxMobilePage(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/mobile/'

    _get_firefox_header_button_locator = (By.ID, 'get-firefox')
    _get_firefox_features_button_locator = (By.ID, 'features-get-firefox')
    _get_firefox_qr_code_locator = (By.ID, 'firefox-qr')

    _get_focus_header_button_locator = (By.ID, 'get-focus')
    _get_focus_features_button_locator = (By.ID, 'features-get-focus')
    _get_focus_qr_code_locator = (By.CSS_SELECTOR, '#focus-qr')

    @property
    def send_to_device(self):
        return SendToDevice(self)

    @property
    def is_firefox_qr_code_displayed(self):
        return self.is_element_displayed(*self._get_firefox_qr_code_locator)

    @property
    def is_focus_qr_code_displayed(self):
        return self.is_element_displayed(*self._get_focus_qr_code_locator)

    def open_modal(self, locator):
        modal = Modal(self)
        self.find_element(*locator).click()
        self.wait.until(lambda s: modal.is_displayed)
        return modal

    def click_get_firefox_button(self):
        self.scroll_element_into_view(*self._get_firefox_header_button_locator)
        return self.open_modal(self._get_firefox_header_button_locator)

    def click_get_focus_button(self):
        self.scroll_element_into_view(*self._get_focus_header_button_locator)
        return self.open_modal(self._get_focus_header_button_locator)

    def click_get_firefox_features_button(self):
        self.scroll_element_into_view(*self._get_firefox_features_button_locator)
        return self.open_modal(self._get_firefox_features_button_locator)

    def click_get_focus_features_button(self):
        self.scroll_element_into_view(*self._get_focus_features_button_locator)
        return self.open_modal(self._get_focus_features_button_locator)
