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

    _create_account_form_locator = (By.ID, 'fxa-email-form')

    @property
    def is_create_account_form_displayed(self):
        wait = Wait(self, timeout=3)
        try:
            result = wait.until(expected.visibility_of_element_located((self._create_account_form_locator)))
            return result
        except TimeoutException:
            return False
