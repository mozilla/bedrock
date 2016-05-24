# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBaseRegion
from pages.firefox.desktop.all import FirefoxDesktopBasePage


class CustomizePage(FirefoxDesktopBasePage):

    URL_TEMPLATE = '/{locale}/firefox/desktop/customize'

    _customize_link_locator = (By.CSS_SELECTOR, '#customizer-list > li')
    _customize_section_locator = (By.CSS_SELECTOR, '#customizers-wrapper > section')
    _theme_button_locator = (By.CSS_SELECTOR, '#themes-thumbs > button')
    _sync_button_locator = (By.ID, 'sync-button')

    @property
    def is_sync_button_displayed(self):
        return self.is_element_displayed(*self._sync_button_locator)

    @property
    def customize_links(self):
        return [CustomizeLink(self, root=el) for el in
                self.find_elements(*self._customize_link_locator)]

    @property
    def customize_sections(self):
        return [CustomizeSection(self, root=el) for el in
                self.find_elements(*self._customize_section_locator)]

    @property
    def themes(self):
        return [Theme(self, root=el) for el in
                self.find_elements(*self._theme_button_locator)]


class CustomizeLink(FirefoxBaseRegion):

    _customize_link_locator = (By.CLASS_NAME, 'show-customizer')

    def click(self):
        section = next(s for s in self.page.customize_sections if s.is_displayed)
        self.scroll_element_into_view(*self._customize_link_locator).click()
        self.wait.until(lambda s: not section.is_displayed)

    @property
    def is_selected(self):
        return 'selected' in self.find_element(
            *self._customize_link_locator).get_attribute('class')


class CustomizeSection(FirefoxBaseRegion):

    _next_link_locator = (By.CLASS_NAME, 'next')

    def click_next(self):
        self.scroll_element_into_view(*self._next_link_locator).click()
        self.wait.until(lambda s: not self.is_displayed)

    @property
    def is_displayed(self):
        return self.root.is_displayed()


class Theme(FirefoxBaseRegion):

    _theme_thumbs_locator = (By.ID, 'themes-thumbs')
    _theme_demo_image_locator = (By.ID, 'theme-demo')

    @property
    def is_image_displayed(self):
        theme = self.root.get_attribute('id')
        image = self.page.find_element(*self._theme_demo_image_locator)
        return (theme in image.get_attribute('src') and
                self.page.is_element_displayed(*self._theme_demo_image_locator))

    @property
    def is_selected(self):
        return 'selected' in self.root.get_attribute('class')

    def click_button(self):
        self.page.scroll_element_into_view(*self._theme_thumbs_locator)
        self.root.click()
        self.wait.until(lambda s: self.is_image_displayed)
