# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage


class InstallerHelpPage(FirefoxBasePage):

    _url = '{base_url}/{locale}/firefox/installer-help'

    _firefox_download_button_locator = (By.CSS_SELECTOR, '#download-button-desktop-release .download-link')
    _beta_download_button_locator = (By.CSS_SELECTOR, '#download-button-desktop-beta .download-link')
    _dev_edition_download_button_locator = (By.CSS_SELECTOR, '#download-button-desktop-alpha .download-link')

    @property
    def is_firefox_download_button_displayed(self):
        return self.download_button(self._firefox_download_button_locator).is_displayed()

    @property
    def is_beta_download_button_displayed(self):
        return self.download_button(self._beta_download_button_locator).is_displayed()

    @property
    def is_dev_edition_download_button_displayed(self):
        return self.download_button(self._dev_edition_download_button_locator).is_displayed()
