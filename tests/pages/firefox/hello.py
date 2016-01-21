# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage
from pages.regions.modal import Modal


class HelloPage(FirefoxBasePage):

    _url = '{base_url}/{locale}/firefox/hello'

    _video_locator = (By.ID, 'video-link')
    _try_hello_button_locator = (By.ID, 'try-hello-footer')
    _download_button_locator = (By.CSS_SELECTOR, '#download-fx .download-link')

    @property
    def is_try_hello_button_displayed(self):
        return self.is_element_displayed(self._try_hello_button_locator)

    @property
    def is_download_button_displayed(self):
        return self.download_button(self._download_button_locator).is_displayed()

    def play_video(self):
        modal = Modal(self)
        self.find_element(self._video_locator).click()
        self.wait.until(lambda s: modal.is_displayed)
        return modal
