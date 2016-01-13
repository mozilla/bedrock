# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class ThunderbirdPage(BasePage):

    _url = '{base_url}/{locale}/thunderbird'

    _download_button_locator = (By.ID, 'download-button-desktop-release')

    @property
    def is_download_button_displayed(self):
        return self.is_element_displayed(self._download_button_locator)
