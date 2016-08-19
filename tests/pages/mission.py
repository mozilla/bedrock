# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class MissionPage(BasePage):

    URL_TEMPLATE = '/{locale}/mission/'

    _video_overlay_locator = (By.CSS_SELECTOR, '.moz-video-container > .moz-video-button')
    _video_locator = (By.CSS_SELECTOR, '.moz-video-container > video')

    @property
    def is_video_overlay_displayed(self):
        return self.is_element_displayed(*self._video_overlay_locator)

    @property
    def is_video_displayed(self):
        return self.is_element_displayed(*self._video_locator)

    def play_video(self):
        assert self.is_video_overlay_displayed, 'Video is already displayed'
        self.find_element(*self._video_overlay_locator).click()
        self.wait.until(lambda m: not self.is_video_overlay_displayed)
