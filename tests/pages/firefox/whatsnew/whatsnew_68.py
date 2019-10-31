# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage


class FirefoxWhatsNew68Page(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/68.0/whatsnew/all/{params}'

    _firefox_accounts_form_locator = (By.ID, 'fxa-email-form')
    _monitor_button_locator = (By.CLASS_NAME, 'js-monitor-button')

    def wait_for_page_to_load(self):
        self.wait.until(lambda s: self.seed_url in s.current_url)
        el = self.find_element(By.TAG_NAME, 'body')
        self.wait.until(lambda s: 'state-fxa-default' not in el.get_attribute('class'))
        return self

    @property
    def is_firefox_accounts_form_displayed(self):
        return self.is_element_displayed(*self._firefox_accounts_form_locator)

    @property
    def is_monitor_button_displayed(self):
        return self.is_element_displayed(*self._monitor_button_locator)
