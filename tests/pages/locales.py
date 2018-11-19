# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class LocalesPage(BasePage):

    URL_TEMPLATE = '/locales/'

    _america_locales_locator = (By.CSS_SELECTOR, '#america ul > li > a')
    _asia_pacific_locales_locator = (By.CSS_SELECTOR, '#asia-pacific ul > li > a')
    _europe_locales_locator = (By.CSS_SELECTOR, '#europe ul > li > a')
    _middle_east_locales_locator = (By.CSS_SELECTOR, '#middle-east ul > li > a')

    @property
    def number_of_america_locales(self):
        return len(self.find_elements(*self._america_locales_locator))

    @property
    def number_of_asia_pacific_locales(self):
        return len(self.find_elements(*self._asia_pacific_locales_locator))

    @property
    def number_of_europe_locales(self):
        return len(self.find_elements(*self._europe_locales_locator))

    @property
    def number_of_middle_east_locales(self):
        return len(self.find_elements(*self._middle_east_locales_locator))
