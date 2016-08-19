# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.regions.download_button import DownloadButton


class InternetHealthPage(BasePage):

    URL_TEMPLATE = '/{locale}/internet-health/'

    _download_button_locator = (By.ID, 'global-nav-download-firefox')

    @property
    def download_button(self):
        el = self.find_element(*self._download_button_locator)
        return DownloadButton(self, root=el)
