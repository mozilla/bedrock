# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.contribute.base import ContributeBasePage


class TwitterTaskPage(ContributeBasePage):

    URL_TEMPLATE = '/{locale}/contribute/task/follow-mozilla/'

    _share_button_locator = (By.CSS_SELECTOR, 'a[data-action="tweet"]')
    _follow_button_locator = (By.CSS_SELECTOR, 'a[data-action="follow"]')

    @property
    def is_share_button_displayed(self):
        return self.is_element_displayed(*self._share_button_locator)

    @property
    def is_follow_button_displayed(self):
        return self.is_element_displayed(*self._follow_button_locator)
