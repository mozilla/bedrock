from __future__ import absolute_import
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pypom import Page, Region
from .regions.newsletter import NewsletterEmbedForm, LegacyNewsletterEmbedForm


class BasePage(Page):

    URL_TEMPLATE = '/{locale}/'

    def __init__(self, selenium, base_url, locale='en-US', **url_kwargs):
        super(BasePage, self).__init__(selenium, base_url, locale=locale, **url_kwargs)

    def wait_for_page_to_load(self):
        self.wait.until(lambda s: self.seed_url in s.current_url)
        el = self.find_element(By.TAG_NAME, 'html')
        self.wait.until(lambda s: 'loaded' in el.get_attribute('class'))
        return self

    @property
    def navigation(self):
        return self.Navigation(self)

    @property
    def footer(self):
        return self.Footer(self)

    @property
    def newsletter(self):
        return NewsletterEmbedForm(self)

    @property
    def legacy_newsletter(self):
        return LegacyNewsletterEmbedForm(self)

    class Navigation(Region):

        _root_locator = (By.CLASS_NAME, 'mzp-c-navigation')
        _toggle_locator = (By.CLASS_NAME, 'mzp-c-navigation-menu-button')
        _menu_locator = (By.CLASS_NAME, 'mzp-c-navigation-items')
        _firefox_menu_locator = (By.CSS_SELECTOR, '.mzp-c-menu-title[aria-controls="mzp-c-menu-panel-firefox"]')
        _projects_menu_locator = (By.CSS_SELECTOR, '.mzp-c-menu-title[aria-controls="mzp-c-menu-panel-projects"]')
        _developers_menu_locator = (By.CSS_SELECTOR, '.mzp-c-menu-title[aria-controls="mzp-c-menu-panel-developers"]')
        _about_menu_locator = (By.CSS_SELECTOR, '.mzp-c-menu-title[aria-controls="mzp-c-menu-panel-about"]')
        _firefox_desktop_page_locator = (By.CSS_SELECTOR, '.mzp-c-menu-item-link[data-link-name="Firefox Quantum Desktop Browser"]')
        _developer_edition_page_locator = (By.CSS_SELECTOR, '.mzp-c-menu-item-link[data-link-name="Firefox Developer Edition"]')
        _about_page_locator = (By.CSS_SELECTOR, '.mzp-c-menu-item-link[data-link-name="Mozilla"]')

        def show(self):
            assert not self.is_displayed, 'Menu is already displayed'
            self.find_element(*self._toggle_locator).click()
            self.wait.until(lambda s: self.is_displayed)
            return self

        @property
        def is_displayed(self):
            toggle = self.find_element(*self._toggle_locator)
            return (self.find_element(*self._menu_locator).is_displayed() and
                'is-active' in toggle.get_attribute('class'))

        def open_navigation_menu(self, locator):
            firefox_menu = self.find_element(*locator)
            firefox_menu.click()
            self.wait.until(lambda s: firefox_menu.is_displayed)

        def open_firefox_desktop_page(self):
            self.open_navigation_menu(self._firefox_menu_locator)
            self.find_element(*self._firefox_desktop_page_locator).click()
            from .firefox.home import FirefoxHomePage
            return FirefoxHomePage(self.selenium, self.page.base_url).wait_for_page_to_load()

        def open_developer_edition_page(self):
            self.open_navigation_menu(self._developers_menu_locator)
            self.find_element(*self._developer_edition_page_locator).click()
            from .firefox.developer import DeveloperPage
            return DeveloperPage(self.selenium, self.page.base_url).wait_for_page_to_load()

        def open_about_page(self):
            self.open_navigation_menu(self._about_menu_locator)
            self.find_element(*self._about_page_locator).click()
            from .about import AboutPage
            return AboutPage(self.selenium, self.page.base_url).wait_for_page_to_load()

    class Footer(Region):

        _root_locator = (By.ID, 'colophon')
        _language_locator = (By.ID, 'page-language-select')

        @property
        def language(self):
            select = self.find_element(*self._language_locator)
            option = select.find_element(By.CSS_SELECTOR, 'option[selected]')
            return option.get_attribute('value')

        @property
        def languages(self):
            el = self.find_element(*self._language_locator)
            return [o.get_attribute('value') for o in Select(el).options]

        def select_language(self, value):
            el = self.find_element(*self._language_locator)
            Select(el).select_by_value(value)
            self.wait.until(lambda s: '/{0}/'.format(value) in s.current_url)
