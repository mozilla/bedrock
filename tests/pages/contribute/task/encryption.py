# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.contribute.base import ContributeBasePage


class EncryptionTaskPage(ContributeBasePage):

    URL_TEMPLATE = '/{locale}/contribute/task/encryption/'

    _take_the_pledge_button_locator = (By.CSS_SELECTOR, 'a[data-task="encryption"]')

    @property
    def is_take_the_pledge_button_displayed(self):
        return self.is_element_displayed(*self._take_the_pledge_button_locator)
