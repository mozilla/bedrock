# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage


class FirefoxOSBasePage(FirefoxBasePage):

    _url = '{base_url}/{locale}/firefox/os/{version}'

    _primary_signup_button = (By.CSS_SELECTOR, '.fxos-cta .primary-cta-signup')
    _primary_get_phone_button = (By.CSS_SELECTOR, '.fxos-cta .primary-cta-phone')
    _news_links_locator = (By.CSS_SELECTOR, '.fxos-news ul > li > a')

    @property
    def is_primary_signup_button_present(self):
        return self.is_element_present(self._primary_signup_button)

    @property
    def is_primary_get_phone_button_present(self):
        return self.is_element_present(self._primary_get_phone_button)

    @property
    def is_news_displayed(self):
        return self.is_element_displayed(self._news_links_locator)
