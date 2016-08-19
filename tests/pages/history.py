# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class HistoryPage(BasePage):

    URL_TEMPLATE = '/{locale}/about/history/'

    _slideshow_locator = (By.CSS_SELECTOR, '#slideshow')
    _previous_button_locator = (By.CSS_SELECTOR, '.slide-control > .prev')
    _next_button_locator = (By.CSS_SELECTOR, '.slide-control > .next')

    @property
    def is_slideshow_displayed(self):
        return 'on' in self.find_element(*self._slideshow_locator).get_attribute('class')

    @property
    def is_previous_button_displayed(self):
        return self.is_element_displayed(*self._previous_button_locator)

    @property
    def is_next_button_displayed(self):
        return self.is_element_displayed(*self._next_button_locator)
