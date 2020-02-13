# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pypom import Region
from selenium.webdriver.common.by import By


class DownloadButton(Region):

    _download_link_locator = (By.CSS_SELECTOR, '.download-link')

    @property
    def _platform_link(self):
        els = [el for el in self.find_elements(*self._download_link_locator)
               if el.is_displayed()]
        assert len(els) == 1, 'Expected one platform link to be displayed'
        return els[0]

    @property
    def is_displayed(self):
        return self.root.is_displayed() and self._platform_link.is_displayed() or False

    @property
    def is_transitional_link(self):
        return '/firefox/download/thanks/' in self._platform_link.get_attribute('href')

    def click(self):
        self._platform_link.click()
