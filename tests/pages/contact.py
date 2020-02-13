# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pypom import Region
from selenium.webdriver.common.by import By

from pages.base import BasePage


class ContactPage(BasePage):

    URL_TEMPLATE = '/{locale}/contact/'

    _contact_tab_locator = (By.CSS_SELECTOR, '.category-tabs > li[data-id=contact]')
    _spaces_tab_locator = (By.CSS_SELECTOR, '.category-tabs > li[data-id=spaces]')
    _communities_tab_locator = (By.CSS_SELECTOR, '.category-tabs > li[data-id=communities]')
    _mobile_menu_toggle_locator = (By.CSS_SELECTOR, '.mzp-c-sidemenu-summary.mzp-js-toggle')

    @property
    def contact_tab(self):
        el = self.find_element(*self._contact_tab_locator)
        return self.Tab(self, root=el)

    @property
    def spaces_tab(self):
        el = self.find_element(*self._spaces_tab_locator)
        return self.Tab(self, root=el)

    @property
    def communities_tab(self):
        el = self.find_element(*self._communities_tab_locator)
        return self.Tab(self, root=el)

    @property
    def is_mobile_menu_toggle_displayed(self):
        return self.is_element_displayed(*self._mobile_menu_toggle_locator)

    class Tab(Region):

        @property
        def is_selected(self):
            return 'current' in self.root.get_attribute('class')


class SpacesPage(ContactPage):

    URL_TEMPLATE = '/{locale}/contact/spaces/{slug}'

    _map_locator = (By.ID, 'map')
    _nav_locator = (By.CSS_SELECTOR, '#nav-spaces li h4')

    @property
    def is_nav_displayed(self):
        return self.is_element_displayed(*self._nav_locator)

    @property
    def spaces(self):
        return [self.Space(self, root=el) for el in self.find_elements(*self._nav_locator)]

    def open_spaces_mobile_menu(self):
        self.find_element(*self._mobile_menu_toggle_locator).click()
        self.wait.until(lambda s: self.is_nav_displayed)

    class Space(Region):

        @property
        def id(self):
            return self.root.get_attribute('data-id')

        @property
        def is_selected(self):
            return 'mzp-is-current' in self.root.get_attribute('class')


class CommunitiesPage(ContactPage):

    URL_TEMPLATE = '/{locale}/contact/communities/{slug}'

    _nav_locator = (By.CSS_SELECTOR, '#nav-communities .region')

    @property
    def is_nav_displayed(self):
        return self.is_element_displayed(*self._nav_locator)

    @property
    def regions(self):
        return [self.Region(self, root=el) for el in self.find_elements(*self._nav_locator)]

    def open_communities_mobile_menu(self):
        self.find_element(*self._mobile_menu_toggle_locator).click()
        self.wait.until(lambda s: self.is_nav_displayed)

    class Region(Region):

        _communities_locator = (By.CSS_SELECTOR, '.submenu li')

        @property
        def id(self):
            return self.root.get_attribute('data-id')

        @property
        def communities(self):
            return [self.Community(self.page, root=el) for el in self.find_elements(*self._communities_locator)]

        @property
        def is_selected(self):
            return 'mzp-is-current' in self.root.get_attribute('class')

        class Community(Region):

            _link_locator = (By.TAG_NAME, 'a')

            @property
            def id(self):
                return self.root.get_attribute('data-id')

            @property
            def is_displayed(self):
                return self.is_element_displayed(*self._link_locator)

            @property
            def is_selected(self):
                return 'mzp-is-current' in self.root.get_attribute('class')
