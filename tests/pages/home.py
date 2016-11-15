# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.regions.download_button import DownloadButton


class HomePage(BasePage):

    _take_over_locator = (By.ID, 'fundraising_takeover')
    _take_over_close_button_locator = (By.ID, 'close_takeover')
    _download_button_locator = (By.ID, 'nav-download-firefox')
    _get_firefox_link_locator = (By.ID, 'fx-download-link')

    @property
    def is_take_over_displayed(self):
        return self.is_element_displayed(*self._take_over_locator)

    def wait_for_page_to_load(self):
        super(BasePage, self).wait_for_page_to_load()
        el = self.find_element(By.TAG_NAME, 'html')
        self.wait.until(lambda s: 'eoy-takeover' in el.get_attribute('class'))
        if self.is_take_over_displayed:
            self.find_element(*self._take_over_close_button_locator).click()
            self.wait.until(lambda s: not self.is_take_over_displayed)
        return self

    @property
    def download_button(self):
        el = self.find_element(*self._download_button_locator)
        return DownloadButton(self, root=el)

    @property
    def is_get_firefox_link_displayed(self):
        return self.is_element_displayed(*self._get_firefox_link_locator)
