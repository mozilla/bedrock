# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage
from pages.regions.download_button import DownloadButton


class AccountsFeaturesPage(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/accounts/features'

    _create_account_button_locator = (By.ID, 'features-header-account')
    _download_button_locator = (By.ID, 'features-header-download')

    def wait_for_page_to_load(self):
        super(FirefoxBasePage, self).wait_for_page_to_load()
        el = self.find_element(By.TAG_NAME, 'html')
        self.wait.until(lambda s: 'state-fxa-default' not in el.get_attribute('class'))
        return self

    @property
    def download_button(self):
        el = self.find_element(*self._download_button_locator)
        return DownloadButton(self, root=el)

    @property
    def is_create_account_button_displayed(self):
        return self.is_element_displayed(*self._create_account_button_locator)
