# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage, FirefoxBaseRegion
from pages.regions.send_to_device import SendToDevice


class AndroidPage(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/android'

    _customize_locator = (By.CSS_SELECTOR, '#customize-accordion > .customize-section')
    _next_button_locator = (By.ID, 'customize-next')
    _previous_button_locator = (By.ID, 'customize-prev')
    _play_store_button_locator = (By.CSS_SELECTOR, '#intro .dl-button')

    @property
    def send_to_device(self):
        return SendToDevice(self)

    @property
    def customize_sections(self):
        return [CustomizeSection(self, root=el) for el in
                self.find_elements(*self._customize_locator)]

    @property
    def current_customize_section(self):
        return next(s for s in self.customize_sections if s.is_displayed)

    def show_next_customize_section(self):
        section = self.current_customize_section
        self.scroll_element_into_view(*self._next_button_locator).click()
        self.wait.until(lambda s:
            self.is_next_enabled and self.is_previous_enabled and not section.is_displayed)

    def show_previous_customize_section(self):
        section = self.current_customize_section
        self.scroll_element_into_view(*self._previous_button_locator).click()
        self.wait.until(lambda s:
            self.is_next_enabled and self.is_previous_enabled and not section.is_displayed)

    @property
    def is_next_enabled(self):
        return self.find_element(*self._next_button_locator).is_enabled()

    @property
    def is_previous_enabled(self):
        return self.find_element(*self._previous_button_locator).is_enabled()

    @property
    def is_play_store_button_displayed(self):
        return self.is_element_displayed(*self._play_store_button_locator)


class CustomizeSection(FirefoxBaseRegion):

    _heading_locator = (By.CSS_SELECTOR, 'h3[role="tab"]')
    _detail_locator = (By.CSS_SELECTOR, 'div[role="tabpanel"]')

    def show_detail(self):
        assert not self.is_displayed, 'Detail is already displayed'
        self.scroll_element_into_view(*self._heading_locator).click()
        detail = self.find_element(*self._detail_locator)
        # Wait for aria-hidden attribute value to determine when animation has finished.
        self.wait.until(lambda m: detail.get_attribute('aria-hidden') == 'false')

    def hide_detail(self):
        assert self.is_displayed, 'Detail is already hidden'
        self.scroll_element_into_view(*self._heading_locator).click()
        self.find_element(*self._heading_locator).click()
        detail = self.find_element(*self._detail_locator)
        # Wait for aria-hidden attribute value to determine when animation has finished.
        self.wait.until(lambda m: detail.get_attribute('aria-hidden') == 'true')

    @property
    def is_displayed(self):
        return self.is_element_displayed(*self._detail_locator)
