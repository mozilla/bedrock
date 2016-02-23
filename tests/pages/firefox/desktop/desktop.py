# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.desktop.all import FirefoxDesktopBasePage
from pages.regions.download_button import DownloadButton


class DesktopPage(FirefoxDesktopBasePage):

    _url = '{base_url}/{locale}/firefox/desktop'

    _primary_download_locator = (By.CSS_SELECTOR, '#overview-intro-download-wrapper .download-button')
    _secondary_download_locator = (By.CSS_SELECTOR, '#subscribe-download-wrapper .download-button')

    @property
    def primary_download_button(self):
        el = self.find_element(self._primary_download_locator)
        return DownloadButton(self, root=el)

    def wait_for_page_to_load(self):
        super(FirefoxDesktopBasePage, self).wait_for_page_to_load()
        self.wait.until(lambda s: self.primary_download_button.is_displayed)
        return self
