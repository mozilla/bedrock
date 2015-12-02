# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.os.version.all import FirefoxOSBasePage
from pages.firefox.base import FirefoxBasePageRegion


class FirefoxOSPage(FirefoxOSBasePage):

    _url = '{base_url}/{locale}/firefox/os/2.0'

    _app_group_buttons_locator = (By.CSS_SELECTOR, '.app-group-selector > li')

    @property
    def app_groups(self):
        return [AppGroup(self, root=el) for el in
                self.find_elements(self._app_group_buttons_locator)]


class AppGroup(FirefoxBasePageRegion):

    _link_locator = (By.TAG_NAME, 'a')
    _faded_icons_locator = (By.CSS_SELECTOR, '.apps > .fade')

    def select(self):
        assert not self.is_active, 'App group is already active'
        self.scroll_element_into_view(self._link_locator).click()
        self.wait.until(lambda s: self.is_active and not self.is_filtered)

    @property
    def id(self):
        return self.find_element(self._link_locator).get_attribute('id')

    @property
    def is_active(self):
        return self.find_element(self._link_locator).get_attribute('class') == 'active-state'

    @property
    def is_filtered(self):
        filtered = False
        for icon in self.selenium.find_elements(*self._faded_icons_locator):
            if self.id in icon.get_attribute('class'):
                filtered = True
        return filtered
