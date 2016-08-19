# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage, FirefoxBaseRegion


class FirefoxAllPage(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/all/'

    _search_input_locator = (By.ID, 'language-search-q')
    _submit_button_locator = (By.CSS_SELECTOR, '#language-search button')
    _build_rows_locator = (By.CSS_SELECTOR, '#builds table > tbody > tr')

    @property
    def _builds(self):
        return [Build(self, root=el) for el in
                self.find_elements(*self._build_rows_locator)]

    @property
    def displayed_builds(self):
        return [b for b in self._builds if b.is_displayed]

    def search_for(self, value):
        self.find_element(*self._search_input_locator).send_keys(value)
        self.find_element(*self._submit_button_locator).click()
        expected_builds = [b for b in self._builds if value in b.language.lower()]
        self.wait.until(lambda s: len(expected_builds) == len(self.displayed_builds))


class Build(FirefoxBaseRegion):

    @property
    def language(self):
        return self.root.get_attribute('data-search')

    @property
    def is_displayed(self):
        return self.root.is_displayed()
