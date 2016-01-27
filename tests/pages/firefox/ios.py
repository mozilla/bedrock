# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage
from pages.regions.modal import Modal
from pages.regions.send_to_device import SendToDevice


class IOSPage(FirefoxBasePage):

    _url = '{base_url}/{locale}/firefox/ios'

    _app_store_button_locator = (By.CSS_SELECTOR, '#intro .appstore-badge')
    _get_it_now_button_locator = (By.CSS_SELECTOR, '#intro .send-to-device .send-to')

    @property
    def send_to_device(self):
        return SendToDevice(self)

    @property
    def is_app_store_button_displayed(self):
        return self.is_element_displayed(self._app_store_button_locator)

    @property
    def is_get_it_now_button_displayed(self):
        return self.is_element_displayed(self._get_it_now_button_locator)

    def click_get_it_now(self):
        modal = Modal(self)
        self.find_element(self._get_it_now_button_locator).click()
        self.wait.until(lambda s: modal.is_displayed)
        return modal
