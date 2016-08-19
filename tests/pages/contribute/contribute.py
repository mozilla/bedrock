# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.contribute.base import ContributeBasePage
from pages.regions.modal import Modal


class ContributePage(ContributeBasePage):

    URL_TEMPLATE = '/{locale}/contribute/'

    _video_play_locator = (By.CSS_SELECTOR, '.video-play')

    def play_video(self):
        modal = Modal(self)
        self.find_element(*self._video_play_locator).click()
        self.wait.until(lambda s: modal.is_displayed)
        return modal
