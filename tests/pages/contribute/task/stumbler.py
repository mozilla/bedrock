# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.contribute.base import ContributeBasePage


class StumblerTaskPage(ContributeBasePage):

    URL_TEMPLATE = '/{locale}/contribute/task/stumbler/'

    _stumbler_button_locator = (By.CLASS_NAME, 'stumbler-button')

    @property
    def is_stumbler_button_displayed(self):
        return self.is_element_displayed(*self._stumbler_button_locator)
