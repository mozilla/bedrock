# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class PluginCheckPage(BasePage):

    URL_TEMPLATE = '/{locale}/plugincheck/'

    _not_supported_message_locator = (By.ID, 'not-supported-container')

    @property
    def is_not_supported_message_displayed(self):
        return self.is_element_displayed(*self._not_supported_message_locator)
