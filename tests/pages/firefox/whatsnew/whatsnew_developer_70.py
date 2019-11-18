# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage
from pages.regions.download_button import DownloadButton


class FirefoxWhatsNewDeveloper70Page(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/70.0a2/whatsnew/all/'

    _nightly_download_button_locator = (By.ID, 'footer-download')

    @property
    def nightly_download_button(self):
        el = self.find_element(*self._nightly_download_button_locator)
        return DownloadButton(self, root=el)
