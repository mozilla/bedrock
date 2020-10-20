# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pypom import Page, Region
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pages.regions.newsletter import NewsletterEmbedForm


class ScrollElementIntoView:

    def scroll_element_into_view(self, strategy, locator):
        # scroll elements so they are not beneath the navigation
        offset = {'x': 0, 'y': -100}
        return super(ScrollElementIntoView, self).scroll_element_into_view(
            strategy, locator, **offset)


class BaseRegion(ScrollElementIntoView, Region):
    pass


class BasePage(ScrollElementIntoView, Page):

    def __init__(self, selenium, base_url, locale='en-US', **url_kwargs):
        super(BasePage, self).__init__(selenium, base_url, locale=locale, **url_kwargs)

    def wait_for_page_to_load(self):
        self.wait.until(lambda s: self.seed_url in s.current_url)
        el = self.find_element(By.TAG_NAME, 'html')
        self.wait.until(lambda s: 'loaded' in el.get_attribute('class'))
        return self

    @property
    def URL_TEMPLATE(self):
        if '?' in self._URL_TEMPLATE:
            return f'{self._URL_TEMPLATE}&automation=true'
        else:
            return f'{self._URL_TEMPLATE}?automation=true'

    @property
    def navigation(self):
        return self.Navigation(self)

    @property
    def footer(self):
        return self.Footer(self)

    @property
    def newsletter(self):
        return NewsletterEmbedForm(self)

    class Navigation(BaseRegion):

        _root_locator = (By.CLASS_NAME, 'c-navigation')
        _toggle_locator = (By.CLASS_NAME, 'c-navigation-menu-button')
        _menu_locator = (By.CLASS_NAME, 'c-navigation-items')
        _firefox_menu_locator = (By.CSS_SELECTOR, '.c-menu-title[aria-controls="c-menu-panel-firefox"]')
        _products_menu_locator = (By.CSS_SELECTOR, '.c-menu-title[aria-controls="c-menu-panel-products"]')
        _about_menu_locator = (By.CSS_SELECTOR, '.c-menu-title[aria-controls="c-menu-panel-about"]')
        _innovation_menu_locator = (By.CSS_SELECTOR, '.c-menu-title[aria-controls="c-menu-panel-innovation"]')
        _firefox_desktop_page_locator = (By.CSS_SELECTOR, '.c-menu-item-link[data-link-name="Firefox Desktop Browser"]')
        _developer_edition_page_locator = (By.CSS_SELECTOR, '.c-menu-item-link[data-link-name="Firefox Developer Edition"]')
        _manifesto_page_locator = (By.CSS_SELECTOR, '.c-menu-item-link[data-link-name="Mozilla Manifesto"]')
        _firefox_download_button_locator = (By.CSS_SELECTOR, '#protocol-nav-download-firefox > .download-link')
        _firefox_account_button_locator = (By.CSS_SELECTOR, '.c-navigation-fxa-cta-container > .js-fxa-cta-link')

        @property
        def is_firefox_download_button_displayed(self):
            return self.is_element_displayed(*self._firefox_download_button_locator)

        @property
        def is_firefox_accounts_button_displayed(self):
            return self.is_element_displayed(*self._firefox_account_button_locator)

        def show(self):
            assert not self.is_displayed, 'Menu is already displayed'
            self.find_element(*self._toggle_locator).click()
            self.wait.until(lambda s: self.is_displayed)
            return self

        @property
        def is_displayed(self):
            toggle = self.find_element(*self._toggle_locator)
            return (
                self.find_element(*self._menu_locator).is_displayed() and
                'is-active' in toggle.get_attribute('class')
            )

        def open_navigation_menu(self, locator):
            firefox_menu = self.find_element(*locator)
            firefox_menu.click()
            self.wait.until(lambda s: firefox_menu.is_displayed)

        def open_firefox_desktop_page(self):
            self.open_navigation_menu(self._firefox_menu_locator)
            link = self.find_element(*self._firefox_desktop_page_locator)
            href = link.get_attribute('href')
            self.page.set_attribute(link, att_name='href', att_value=href + '?automation=true')
            link.click()
            from .firefox.new.download import DownloadPage
            return DownloadPage(self.selenium, self.page.base_url).wait_for_page_to_load()

        def open_developer_edition_page(self):
            self.open_navigation_menu(self._innovation_menu_locator)
            self.find_element(*self._developer_edition_page_locator).click()
            from .firefox.developer import DeveloperPage
            return DeveloperPage(self.selenium, self.page.base_url).wait_for_page_to_load()

        def open_manifesto_page(self):
            self.open_navigation_menu(self._about_menu_locator)
            self.find_element(*self._manifesto_page_locator).click()
            from .manifesto import ManifestoPage
            return ManifestoPage(self.selenium, self.page.base_url).wait_for_page_to_load()

    class Footer(BaseRegion):

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
