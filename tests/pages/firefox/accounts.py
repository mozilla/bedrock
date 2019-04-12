# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.ui import WebDriverWait as Wait

from pages.firefox.base import FirefoxBasePage


class FirefoxAccountsPage(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/accounts/'

    _download_buttons_locator = (By.CLASS_NAME, 'features-download')
    _create_account_form_locator = (By.ID, 'fxa-email-form')

    @property
    def is_create_account_form_displayed(self):
        wait = Wait(self, timeout=3)
        try:
            result = wait.until(expected.visibility_of_element_located((self._create_account_form_locator)))
            return result
        except TimeoutException:
            return False

    @property
    def are_download_buttons_displayed(self):
        wait = Wait(self, timeout=3)
        try:
            result = wait.until(expected.visibility_of_all_elements_located((self._download_buttons_locator)))
            return result
        except TimeoutException:
            return False
