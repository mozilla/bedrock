# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from page import Page, PageRegion
from regions.newsletter import NewsletterEmbedForm


class BasePage(Page):

    _url = '{base_url}/{locale}'

    def __init__(self, base_url, selenium, locale='en-US', **kwargs):
        super(BasePage, self).__init__(base_url, selenium, locale=locale, **kwargs)

    def wait_for_page_to_load(self):
        super(BasePage, self).wait_for_page_to_load()
        el = self.find_element((By.TAG_NAME, 'html'))
        self.wait.until(lambda s: 'loaded' in el.get_attribute('class'))
        return self

    @property
    def navigation(self):
        return self.Navigation(self.base_url, self.selenium)

    @property
    def footer(self):
        return self.Footer(self.base_url, self.selenium)

    @property
    def newsletter(self):
        return NewsletterEmbedForm(self.base_url, self.selenium)

    class Navigation(PageRegion):

        _root_locator = (By.ID, 'nav-main')
        _toggle_locator = (By.CLASS_NAME, 'toggle')
        _menu_locator = (By.ID, 'nav-main-menu')
        _about_locator = (By.CSS_SELECTOR, 'a[data-link-type="about"]')
        _participate_locator = (By.CSS_SELECTOR, 'a[data-link-type="participate"]')
        _firefox_locator = (By.CSS_SELECTOR, 'a[data-link-type="firefox"]')

        def show(self):
            assert not self.is_displayed, 'Menu is already displayed'
            self.find_element(self._toggle_locator).click()
            self.wait.until(lambda s: self.is_displayed)
            return self

        @property
        def is_displayed(self):
            toggle = self.find_element(self._toggle_locator)
            return (self.find_element(self._menu_locator).is_displayed() and
                toggle.get_attribute('aria-expanded') == 'true')

        def open_about(self):
            self.find_element(self._about_locator).click()
            from about import AboutPage
            return AboutPage(self.base_url, self.selenium).wait_for_page_to_load()

        def open_participate(self):
            self.find_element(self._participate_locator).click()
            from contribute.contribute import ContributePage
            return ContributePage(self.base_url, self.selenium).wait_for_page_to_load()

        def open_firefox(self):
            self.find_element(self._firefox_locator).click()
            from firefox.products import ProductsPage
            return ProductsPage(self.base_url, self.selenium).wait_for_page_to_load()

    class Footer(PageRegion):

        _root_locator = (By.ID, 'colophon')
        _language_locator = (By.ID, 'page-language-select')

        @property
        def language(self):
            select = self.find_element(self._language_locator)
            option = select.find_element(By.CSS_SELECTOR, 'option[selected]')
            return option.get_attribute('value')

        @property
        def languages(self):
            el = self.find_element(self._language_locator)
            return [o.get_attribute('value') for o in Select(el).options]

        def select_language(self, value):
            el = self.find_element(self._language_locator)
            Select(el).select_by_value(value)
            self.wait.until(lambda s: '/{0}/'.format(value) in s.current_url)
