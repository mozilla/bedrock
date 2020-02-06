# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage


class EnterprisePage(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/enterprise/'

    _primary_download_button_locator = (By.ID, 'primary-download-button')

    @property
    def is_primary_download_button_displayed(self):
        return self.is_element_displayed(*self._primary_download_button_locator)
