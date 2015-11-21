# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage, FirefoxBasePageRegion


class TVPage(FirefoxBasePage):

    _url = '{base_url}/{locale}/firefox/os/devices/tv'

    _next_button_locator = (By.CSS_SELECTOR, '.pager-next')
    _previous_button_locator = (By.CSS_SELECTOR, '.pager-prev')
    _screens_locator = (By.CSS_SELECTOR, '.pager-page')
    _thumbnails_locator = (By.CSS_SELECTOR, '.pager-tabs li')

    @property
    def screens(self):
        return [Screens(self.base_url, self.selenium, root=el) for el in
                self.find_elements(self._screens_locator)]

    @property
    def thumbnails(self):
        return [Thumbnails(self.base_url, self.selenium, root=el) for el in
                self.find_elements(self._thumbnails_locator)]

    def show_next_screen(self):
        screen = next(s for s in self.screens if s.is_displayed)
        self.find_element(self._next_button_locator).click()
        self.wait.until(lambda s: not screen.is_displayed)

    def show_previous_screen(self):
        screen = next(s for s in self.screens if s.is_displayed)
        self.find_element(self._previous_button_locator).click()
        self.wait.until(lambda s: not screen.is_displayed)

    # This method is necessary because the Thumbnails page region
    # does not have a reference to the page object. Perhaps we can
    # improve this in the future.
    def click_thumbnail(self, index):
        screen = next(s for s in self.screens if s.is_displayed)
        self.thumbnails[index].click()
        self.wait.until(lambda s: not screen.is_displayed)

    @property
    def is_next_enabled(self):
        return self.find_element(self._next_button_locator).is_enabled()

    @property
    def is_previous_enabled(self):
        return self.find_element(self._previous_button_locator).is_enabled()


class Screens(FirefoxBasePageRegion):

    _image_locator = (By.TAG_NAME, 'img')

    @property
    def is_displayed(self):
        return self.is_element_displayed(self._image_locator)


class Thumbnails(FirefoxBasePageRegion):

    _link_locator = (By.TAG_NAME, 'a')

    @property
    def is_selected(self):
        return self.find_element(self._link_locator).get_attribute('class') == 'selected'

    def click(self):
        self.find_element(self._link_locator).click()
        self.wait.until(lambda s: self.is_selected)
