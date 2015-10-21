# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.ui import WebDriverWait as Wait

from .base import BasePage


class ContributePage(BasePage):

    _url = '{base_url}/{locale}/contribute'

    _video_play_locator = (By.CSS_SELECTOR, '.video-play')
    _video_close_locator = (By.ID, 'modal-close')
    _video_modal_locator = (By.ID, 'modal')

    _event_link_locator = (By.CSS_SELECTOR, '.extra-event .event-link')

    def play_video(self):
        self.selenium.find_element(*self._video_play_locator).click()
        Wait(self.selenium, self.timeout).until(
            expected.visibility_of_element_located(self._video_modal_locator))

    def close_video(self):
        close = self.selenium.find_element(*self._video_close_locator)
        close.click()
        Wait(self.selenium, self.timeout).until(
            expected.staleness_of(close))

    @property
    def video_modal_is_displayed(self):
        return self.selenium.find_element(*self._video_modal_locator).is_displayed()

    @property
    def next_event_is_displayed(self):
        return self.selenium.find_element(*self._event_link_locator).is_displayed()
