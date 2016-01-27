# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.page import PageRegion


class ContactPage(BasePage):

    _url = '{base_url}/{locale}/contact'

    _map_pins_locator = (By.CSS_SELECTOR, '#map img.leaflet-marker-icon')
    _contact_tab_locator = (By.CSS_SELECTOR, '.category-tabs > li[data-id=contact]')
    _spaces_tab_locator = (By.CSS_SELECTOR, '.category-tabs > li[data-id=spaces]')
    _communities_tab_locator = (By.CSS_SELECTOR, '.category-tabs > li[data-id=communities]')

    @property
    def displayed_map_pins(self):
        return len([el for el in self.find_elements(self._map_pins_locator) if el.is_displayed()])

    @property
    def contact_tab(self):
        el = self.find_element(self._contact_tab_locator)
        return self.Tab(self, root=el)

    @property
    def spaces_tab(self):
        el = self.find_element(self._spaces_tab_locator)
        return self.Tab(self, root=el)

    @property
    def communities_tab(self):
        el = self.find_element(self._communities_tab_locator)
        return self.Tab(self, root=el)

    def click_contact_tab(self):
        self.contact_tab.click()
        return ContactPage(self.base_url, self.selenium).wait_for_page_to_load()

    def click_spaces_tab(self):
        self.spaces_tab.click()
        return SpacesPage(self.base_url, self.selenium).wait_for_page_to_load()

    def click_communities_tab(self):
        self.communities_tab.click()
        return CommunitiesPage(self.base_url, self.selenium).wait_for_page_to_load()

    class Tab(PageRegion):

        _link_locator = (By.TAG_NAME, 'a')

        @property
        def is_selected(self):
            return 'current' in self._root.get_attribute('class')

        def click(self):
            self.find_element(self._link_locator).click()


class SpacesPage(ContactPage):

    _url = '{base_url}/{locale}/contact/spaces'

    _spaces_locator = (By.ID, 'nav-spaces li')

    @property
    def spaces(self):
        return [self.Space(self, root=el) for el in
            self.find_elements(self._spaces_locator)]

    def wait_for_page_to_load(self):
        super(ContactPage, self).wait_for_page_to_load()
        self.wait.until(lambda s: self.displayed_map_pins == len(self.spaces))
        return self

    class Space(PageRegion):

        _link_locator = (By.TAG_NAME, 'a')

        @property
        def is_displayed(self):
            return self.page.is_element_displayed(
                (By.ID, self._root.get_attribute('data-id')))

        @property
        def is_selected(self):
            return 'current' in self._root.get_attribute('class')

        def click(self):
            self.find_element(self._link_locator).click()
            self.wait.until(lambda s: self.is_displayed and
                            self.page.displayed_map_pins == 1)


class CommunitiesPage(ContactPage):

    _url = '{base_url}/{locale}/contact/communities'

    _keys_locator = (By.CSS_SELECTOR, '#map .legend li')
    _regions_locator = (By.CSS_SELECTOR, '#nav-communities .region')

    @property
    def keys(self):
        return [self.Key(self, root=el) for el in
            self.find_elements(self._keys_locator)]

    @property
    def regions(self):
        return [self.Region(self, root=el) for el in
            self.find_elements(self._regions_locator)]

    @property
    def is_communities_legend_displayed(self):
        return self.is_element_displayed(self._keys_locator)

    def wait_for_page_to_load(self):
        super(ContactPage, self).wait_for_page_to_load()
        self.wait.until(lambda s: self.is_communities_legend_displayed)
        return self

    class Key(PageRegion):

        _link_locator = (By.TAG_NAME, 'a')

        @property
        def id(self):
            return self._root.get_attribute('data-id')

        @property
        def is_selected(self):
            el = self.find_element(self._link_locator)
            return 'active' in el.get_attribute('class')

        def click(self):
            self.find_element(self._link_locator).click()
            region = next(r for r in self.page.regions if r.id == self.id)
            self.wait.until(lambda s: region.is_displayed)

    class Region(PageRegion):

        _communities_locator = (By.CSS_SELECTOR, '.submenu li')
        _link_locator = (By.TAG_NAME, 'a')

        @property
        def id(self):
            return self._root.get_attribute('data-id')

        @property
        def communities(self):
            return [self.Community(self.page, root=el) for el in
                self.find_elements(self._communities_locator)]

        @property
        def is_displayed(self):
            return self.page.is_element_displayed((By.ID, self.id))

        @property
        def is_selected(self):
            return 'current' in self._root.get_attribute('class')

        @property
        def is_menu_open(self):
            return 'open' in self._root.get_attribute('class')

        def click(self):
            self.find_element(self._link_locator).click()
            self.wait.until(lambda s: self.is_displayed)

        class Community(PageRegion):

            _link_locator = (By.TAG_NAME, 'a')

            @property
            def id(self):
                return self._root.get_attribute('data-id')

            @property
            def is_displayed(self):
                return self.page.is_element_displayed((By.ID, self.id))

            @property
            def is_selected(self):
                return 'current' in self._root.get_attribute('class')

            def click(self):
                self.find_element(self._link_locator).click()
                self.wait.until(lambda s: self.is_displayed)
