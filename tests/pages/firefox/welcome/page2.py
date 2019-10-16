# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage


class FirefoxWelcomePage2(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/welcome/2/'

    _pocket_button_locator = (By.ID, 'pocket-cta')

    @property
    def is_pocket_button_displayed(self):
        return self.is_element_displayed(*self._pocket_button_locator)
