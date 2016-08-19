# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.smarton.base import SmartOnBasePage


class SmartOnLandingPage(SmartOnBasePage):

    URL_TEMPLATE = '/{locale}/teach/smarton/'

    _topic_tracking_locator = (By.CSS_SELECTOR, '#topic-tracking > a')
    _topic_security_locator = (By.CSS_SELECTOR, '#topic-security > a')
    _topic_surveillance_locator = (By.CSS_SELECTOR, '#topic-surveillance > a')

    def open_tracking(self):
        self.find_element(*self._topic_tracking_locator).click()
        from pages.smarton.base import SmartOnBasePage
        return SmartOnBasePage(self.selenium, self.base_url,
                               slug='tracking').wait_for_page_to_load()

    def open_security(self):
        self.find_element(*self._topic_security_locator).click()
        from pages.smarton.base import SmartOnBasePage
        return SmartOnBasePage(self.selenium, self.base_url,
                               slug='security').wait_for_page_to_load()

    def open_surveillance(self):
        self.find_element(*self._topic_surveillance_locator).click()
        from pages.smarton.base import SmartOnBasePage
        return SmartOnBasePage(self.selenium, self.base_url,
                               slug='surveillance').wait_for_page_to_load()
