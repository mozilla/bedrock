# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.page import PageRegion
from pages.firefox.base import FirefoxBasePage
from pages.regions.modal import Modal


class DeveloperPage(FirefoxBasePage):

    _url = '{base_url}/{locale}/firefox/developer'

    _primary_download_locator = (By.CSS_SELECTOR, '.intro .download-button .download-link')
    _secondary_download_locator = (By.CSS_SELECTOR, '.dev-footer-download .download-button .download-link')
    _videos_locator = (By.CSS_SELECTOR, '.features > .feature > .video-play')

    @property
    def is_primary_download_button_displayed(self):
        return self.download_button(self._primary_download_locator).is_displayed()

    @property
    def is_secondary_download_button_displayed(self):
        return self.download_button(self._secondary_download_locator).is_displayed()

    @property
    def developer_videos(self):
        return [Video(self, root=el) for el in
                self.find_elements(self._videos_locator)]


class Video(PageRegion):

    def play(self):
        modal = Modal(self)
        self._root.click()
        self.wait.until(lambda s: modal.is_displayed)
        return modal
