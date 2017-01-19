# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected

from pages.base import BasePage
from pages.regions.download_button import DownloadButton


class HomePage(BasePage):

    _popup_locator = (By.ID, 'brand-popup')
    _popup_close_button_locator = (By.ID, 'close-brand-popup')
    _download_button_locator = (By.ID, 'nav-download-firefox')
    _get_firefox_link_locator = (By.ID, 'fx-download-link')

    @property
    def is_popup_displayed(self):
        return self.is_element_displayed(*self._popup_close_button_locator)

    def wait_for_page_to_load(self):
        super(BasePage, self).wait_for_page_to_load()
        el = self.find_element(By.TAG_NAME, 'html')
        self.wait.until(lambda s: 'brand-popup-ready' in el.get_attribute('class'))
        popup = self.selenium.find_element(*self._popup_locator)
        if 'show' in popup.get_attribute('class'):
            self.wait.until(lambda s: self.is_popup_displayed)
            self.find_element(*self._popup_close_button_locator).click()
            self.wait.until(expected.staleness_of(popup))
        return self

    @property
    def download_button(self):
        el = self.find_element(*self._download_button_locator)
        return DownloadButton(self, root=el)

    @property
    def is_get_firefox_link_displayed(self):
        return self.is_element_displayed(*self._get_firefox_link_locator)
