# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BaseRegion


class DownloadButton(BaseRegion):
    _download_link_locator = (By.CSS_SELECTOR, ".download-link")

    @property
    def platform_link(self):
        els = [el for el in self.find_elements(*self._download_link_locator) if el.is_displayed()]
        return els[0]

    @property
    def is_displayed(self):
        return self.root.is_displayed() and self.platform_link.is_displayed() or False

    @property
    def is_transitional_link(self):
        return "/firefox/download/thanks/" in self.platform_link.get_attribute("href")

    def click(self):
        self.platform_link.click()
