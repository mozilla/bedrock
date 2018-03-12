# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage


class EnterprisePage(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/enterprise/'

    _primary_cta_locator = (By.ID, 'beta-signup')

    @property
    def primary_cta(self):
        return self.find_element(*self._primary_cta_locator)
