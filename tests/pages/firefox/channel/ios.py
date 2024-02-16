# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class ChannelIOSPage(BasePage):
    _URL_TEMPLATE = "/{locale}/firefox/channel/ios/"

    _testflight_button_locator = (By.CLASS_NAME, "testflight-cta")

    @property
    def is_testflight_button_displayed(self):
        return self.is_element_displayed(*self._testflight_button_locator)
