# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class ThunderbirdChannelPage(BasePage):

    _url = '{base_url}/{locale}/thunderbird/channel'

    _earlybird_download_button_locator = (By.CSS_SELECTOR, '#download-button-desktop-alpha .download-link')
    _beta_download_button_locator = (By.CSS_SELECTOR, '#download-button-desktop-beta .download-link')

    @property
    def is_beta_download_button_displayed(self):
        return self.download_button(self._beta_download_button_locator).is_displayed()

    @property
    def is_earlybird_download_button_displayed(self):
        return self.download_button(self._earlybird_download_button_locator).is_displayed()
