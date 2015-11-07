# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait

from .base import BasePage
from .regions.modal import Modal


class ContributePage(BasePage):

    _url = '{base_url}/{locale}/contribute'

    _video_play_locator = (By.CSS_SELECTOR, '.video-play')
    _event_link_locator = (By.CSS_SELECTOR, '.extra-event .event-link')

    def play_video(self):
        modal = Modal(self.selenium)
        self.selenium.find_element(*self._video_play_locator).click()
        Wait(self.selenium, self.timeout).until(lambda s: modal.is_displayed)
        return modal

    @property
    def next_event_is_displayed(self):
        return self.is_element_displayed(self._event_link_locator)
