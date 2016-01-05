# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class Win10WelcomePage(BasePage):

    _url = '{base_url}/{locale}/firefox/windows-10/welcome'

    _main_contant_locator = (By.TAG_NAME, 'main')
    _links_section_locator = (By.CLASS_NAME, 'firefox-learn-links')

    @property
    def is_firefox_default_messaging_displayed(self):
        el = self.find_element(self._main_contant_locator)
        return 'firefox-default' in el.get_attribute('class')

    @property
    def is_links_section_displayed(self):
        return self.is_element_displayed(self._links_section_locator)
