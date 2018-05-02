# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage


class AccountsFeaturesPage(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/accounts/features'

    _primary_cta_locator = (By.CSS_SELECTOR, '.fab-head-cta .button')

    @property
    def primary_cta(self):
        return self.find_element(*self._primary_cta_locator)
