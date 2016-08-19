# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.contribute.base import ContributeBasePage


class MobileTaskPage(ContributeBasePage):

    URL_TEMPLATE = '/{locale}/contribute/task/firefox-mobile/'

    _android_download_button_locator = (By.CSS_SELECTOR, '.step-content a[data-download-os="Android"]')
    _ios_download_button_locator = (By.CSS_SELECTOR, '.step-content a[data-download-os="iOS"]')

    @property
    def is_android_download_button_displayed(self):
        return self.is_element_displayed(*self._android_download_button_locator)

    @property
    def is_ios_download_button_displayed(self):
        return self.is_element_displayed(*self._ios_download_button_locator)
