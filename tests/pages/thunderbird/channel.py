# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class ThunderbirdChannelPage(BasePage):

    _url = '{base_url}/{locale}/thunderbird/channel'

    _earlybird_download_button_locator = (By.ID, 'download-button-desktop-alpha')
    _beta_download_button_locator = (By.ID, 'download-button-desktop-beta')

    @property
    def is_beta_download_button_displayed(self):
        return self.is_element_displayed(self._beta_download_button_locator)

    @property
    def is_earlybird_download_button_displayed(self):
        return self.is_element_displayed(self._earlybird_download_button_locator)
