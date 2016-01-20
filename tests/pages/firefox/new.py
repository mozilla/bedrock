# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage


class FirefoxNewPage(FirefoxBasePage):

    _url = '{base_url}/{locale}/firefox/new/'

    _download_button_locator = (By.CSS_SELECTOR, '#features-download .download-button .download-link')
    _thank_you_message_locator = (By.ID, 'scene2-main')

    @property
    def is_download_button_displayed(self):
        return self.download_button(self._download_button_locator).is_displayed()

    def download_firefox(self):
        self.download_button(self._download_button_locator).click()
        self.wait.until(lambda s: self.is_thank_you_message_displayed)

    @property
    def is_thank_you_message_displayed(self):
        return self.is_element_displayed(self._thank_you_message_locator)


class FirefoxNewThankYouPage(FirefoxNewPage):

    _url = '{base_url}/{locale}/firefox/new/?scene=2#download-fx'

    def wait_for_page_to_load(self):
        super(FirefoxNewPage, self).wait_for_page_to_load()
        self.wait.until(lambda s: self.is_thank_you_message_displayed)
        return self
