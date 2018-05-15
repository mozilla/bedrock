# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage


class EnterprisePage(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/enterprise/'

    _signup_button_locator = (By.CSS_SELECTOR, '.qa-sign-up')
    _download_release_locator = (By.CSS_SELECTOR, '.qa-download-release')
    _download_esr_locator = (By.CSS_SELECTOR, '.qa-download-esr')

    @property
    def signup_button(self):
        return self.find_element(*self._signup_button_locator)

    @property
    def download_release_link(self):
        return self.find_element(*self._download_release_locator)

    @property
    def download_esr_link(self):
        return self.find_element(*self._download_esr_locator)
