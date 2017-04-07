# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage


class ThankYouPage(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/new/?scene=2'

    _direct_download_link_locator = (By.ID, 'direct-download-link')

    # Bug 1354334 - sometimes download is triggered before window.load.
    def wait_for_page_to_load(self):
        self.wait.until(lambda s: self.seed_url in s.current_url)
        el = self.find_element(By.TAG_NAME, 'html')
        self.wait.until(lambda s: 'download-ready' in el.get_attribute('class'))
        return self

    @property
    def is_direct_download_link_displayed(self):
        return self.is_element_displayed(*self._direct_download_link_locator)

    @property
    def is_direct_download_link_valid(self):
        return 'https://download.mozilla.org' in self.find_element(
            *self._direct_download_link_locator).get_attribute('href')
