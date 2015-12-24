# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage


class FirefoxSyncPage(FirefoxBasePage):

    _url = '{base_url}/{locale}/firefox/sync'

    _primary_download_button_locator = (By.ID, 'download-button-desktop-release')
    _android_download_button_locator = (By.ID, 'cta-android-footer')

    @property
    def is_primary_download_button_displayed(self):
        return self.is_element_displayed(self._primary_download_button_locator)

    @property
    def is_android_download_button_displayed(self):
        return self.is_element_displayed(self._android_download_button_locator)
