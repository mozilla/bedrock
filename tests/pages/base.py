# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from pypom import Page, Region
from selenium.webdriver.common.by import By


class ScrollElementIntoView:
    def scroll_element_into_view(self, strategy, locator):
        # scroll elements so they are not beneath the navigation
        offset = {"x": 0, "y": -100}
        return super().scroll_element_into_view(strategy, locator, **offset)


class BaseRegion(ScrollElementIntoView, Region):
    pass


class BasePage(ScrollElementIntoView, Page):
    def __init__(self, selenium, base_url, locale="en-US", **url_kwargs):
        super().__init__(selenium, base_url, locale=locale, **url_kwargs)

    def wait_for_page_to_load(self):
        self.wait.until(lambda s: self.seed_url in s.current_url)
        el = self.find_element(By.TAG_NAME, "html")
        self.wait.until(lambda s: "loaded" in el.get_attribute("class"))
        return self

    @property
    def URL_TEMPLATE(self):
        if "{params}" in self._URL_TEMPLATE:
            return f"{self._URL_TEMPLATE}&automation=true"
        else:
            return f"{self._URL_TEMPLATE}?automation=true"

    @property
    def navigation(self):
        return self.Navigation(self)

    class Navigation(BaseRegion):
        _root_locator = (By.CLASS_NAME, "m24-navigation-refresh")
        _toggle_locator = (By.CLASS_NAME, "m24-c-navigation-menu-button")
        _menu_locator = (By.CLASS_NAME, "m24-c-navigation-items")
        _products_menu_link_locator = (By.CSS_SELECTOR, '.m24-c-menu-title[aria-controls="m24-c-menu-panel-products"]')
        _products_menu_locator = (By.ID, "m24-c-menu-panel-products")
        _about_menu_link_locator = (By.CSS_SELECTOR, '.m24-c-menu-title[aria-controls="m24-c-menu-panel-about"]')
        _about_menu_locator = (By.ID, "m24-c-menu-panel-about")

        @property
        def is_displayed(self):
            toggle = self.find_element(*self._toggle_locator)
            return self.find_element(*self._menu_locator).is_displayed() and "is-active" in toggle.get_attribute("class")

        def open_navigation_menu(self, locator):
            menu = self.find_element(*locator)
            menu.click()

        @property
        def is_products_menu_displayed(self):
            return self.is_element_displayed(*self._products_menu_locator)

        @property
        def is_about_menu_displayed(self):
            return self.is_element_displayed(*self._about_menu_locator)

        def open_products_menu(self):
            self.open_navigation_menu(self._products_menu_link_locator)
            self.wait.until(lambda s: self.is_products_menu_displayed)

        def open_about_menu(self):
            self.open_navigation_menu(self._about_menu_link_locator)
            self.wait.until(lambda s: self.is_about_menu_displayed)
