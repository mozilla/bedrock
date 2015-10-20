# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait as Wait

from .page import Page, PageRegion


class BasePage(Page):

    _url = '{base_url}/{locale}'

    def wait_for_page_to_load(self):
        el = self.selenium.find_element(By.TAG_NAME, 'html')
        Wait(self.selenium, self.timeout).until(
            lambda s: 'loaded' in el.get_attribute('class'))
        return self

    @property
    def footer(self):
        return self.Footer(self.selenium)

    class Footer(PageRegion):

        _root_locator = (By.ID, 'colophon')
        _language_locator = (By.ID, 'page-language-select')

        @property
        def language(self):
            select = self.root.find_element(*self._language_locator)
            option = select.find_element(By.CSS_SELECTOR, 'option[selected]')
            return option.get_attribute('value')

        @property
        def languages(self):
            el = self.root.find_element(*self._language_locator)
            return [o.get_attribute('value') for o in Select(el).options]

        def select_language(self, value):
            el = self.root.find_element(*self._language_locator)
            Select(el).select_by_value(value)
            Wait(self.selenium, self.timeout).until(
                lambda s: value in s.current_url)
