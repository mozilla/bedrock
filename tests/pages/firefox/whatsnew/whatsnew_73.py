# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class FirefoxWhatsNew73Page(BasePage):

    URL_TEMPLATE = '/{locale}/firefox/73.0/whatsnew/all/{params}'

    _set_default_button_locator = (By.ID, 'set-as-default-button')

    @property
    def is_default_browser_button_displayed(self):
        return self.is_element_displayed(*self._set_default_button_locator)
