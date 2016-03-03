# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage
from pages.regions.download_button import DownloadButton


class DownloadPage(FirefoxBasePage):

    _url = '{base_url}/{locale}/firefox/new/'

    _download_button_locator = (By.ID, 'download-button-desktop-release')

    @property
    def download_button(self):
        el = self.find_element(self._download_button_locator)
        return DownloadButton(self, root=el)

    def download_firefox(self):
        self.download_button.click()
        from pages.firefox.new.thank_you import ThankYouPage
        return ThankYouPage(self.base_url, self.selenium).wait_for_page_to_load()
