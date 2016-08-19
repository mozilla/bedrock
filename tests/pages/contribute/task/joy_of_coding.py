# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.contribute.base import ContributeBasePage


class JoyOfCodingTaskPage(ContributeBasePage):

    URL_TEMPLATE = '/{locale}/contribute/task/joy-of-coding/'

    _video_locator = (By.ID, 'joc')
    _watch_the_video_button_locator = (By.CSS_SELECTOR, 'button[data-task="joyofcoding"]')

    @property
    def is_video_displayed(self):
        return self.is_element_displayed(*self._video_locator)

    @property
    def is_watch_the_video_button_displayed(self):
        return self.is_element_displayed(*self._watch_the_video_button_locator)
