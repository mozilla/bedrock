# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from base import BasePage


class PluginCheckPage(BasePage):

    _url = '{base_url}/{locale}/plugincheck'

    _not_supported_message_locator = (By.CLASS_NAME, 'not-supported')

    @property
    def is_not_supported_message_displayed(self):
        return self.is_element_displayed(self._not_supported_message_locator)
