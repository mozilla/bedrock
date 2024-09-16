# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from pypom import Page, Region
from selenium.webdriver.common.by import By

from pages.regions.newsletter import NewsletterEmbedForm


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

    @property
    def newsletter(self):
        return NewsletterEmbedForm(self)

    class Navigation(BaseRegion):
        _root_locator = (By.CLASS_NAME, "c-navigation")
        _toggle_locator = (By.CLASS_NAME, "c-navigation-menu-button")
        _menu_locator = (By.CLASS_NAME, "c-navigation-items")
        _firefox_menu_link_locator = (By.CSS_SELECTOR, '.c-menu-title[aria-controls="c-menu-panel-firefox"]')
        _firefox_menu_locator = (By.ID, "c-menu-panel-firefox")
        _products_menu_link_locator = (By.CSS_SELECTOR, '.c-menu-title[aria-controls="c-menu-panel-products"]')
        _products_menu_locator = (By.ID, "c-menu-panel-products")
        _about_menu_link_locator = (By.CSS_SELECTOR, '.c-menu-title[aria-controls="c-menu-panel-about"]')
        _about_menu_locator = (By.ID, "c-menu-panel-about")
        _innovation_menu_link_locator = (By.CSS_SELECTOR, '.c-menu-title[aria-controls="c-menu-panel-innovation"]')
        _innovation_menu_locator = (By.ID, "c-menu-panel-innovation")
        _firefox_download_button_locator = (By.CSS_SELECTOR, "#protocol-nav-download-firefox > .download-link")
        _mozilla_vpn_button_locator = (By.CSS_SELECTOR, '.c-navigation-vpn-cta-container > [data-cta-text="Get Mozilla VPN"]')

        @property
        def is_firefox_download_button_displayed(self):
            return self.is_element_displayed(*self._firefox_download_button_locator)

        @property
        def is_mozilla_vpn_button_displayed(self):
            return self.is_element_displayed(*self._mozilla_vpn_button_locator)

        def show(self):
            assert not self.is_displayed, "Menu is already displayed"
            self.find_element(*self._toggle_locator).click()
            self.wait.until(lambda s: self.is_displayed)
            return self

        @property
        def is_displayed(self):
            toggle = self.find_element(*self._toggle_locator)
            return self.find_element(*self._menu_locator).is_displayed() and "is-active" in toggle.get_attribute("class")

        def open_navigation_menu(self, locator):
            menu = self.find_element(*locator)
            menu.click()

        @property
        def is_firefox_menu_displayed(self):
            return self.is_element_displayed(*self._firefox_menu_locator)

        @property
        def is_products_menu_displayed(self):
            return self.is_element_displayed(*self._products_menu_locator)

        @property
        def is_about_menu_displayed(self):
            return self.is_element_displayed(*self._about_menu_locator)

        @property
        def is_innovation_menu_displayed(self):
            return self.is_element_displayed(*self._innovation_menu_locator)

        def open_firefox_menu(self):
            self.open_navigation_menu(self._firefox_menu_link_locator)
            self.wait.until(lambda s: self.is_firefox_menu_displayed)

        def open_products_menu(self):
            self.open_navigation_menu(self._products_menu_link_locator)
            self.wait.until(lambda s: self.is_products_menu_displayed)

        def open_about_menu(self):
            self.open_navigation_menu(self._about_menu_link_locator)
            self.wait.until(lambda s: self.is_about_menu_displayed)

        def open_innovation_menu(self):
            self.open_navigation_menu(self._innovation_menu_link_locator)
            self.wait.until(lambda s: self.is_innovation_menu_displayed)
