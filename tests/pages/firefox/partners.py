# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage, FirefoxBasePageRegion
from pages.regions.modal import Modal


class PartnersPage(FirefoxBasePage):

    _url = '{base_url}/{locale}/firefox/partners'
    _firefox_os_locator = (By.ID, 'os')
    _marketplace_locator = (By.ID, 'marketplace')
    _android_locator = (By.ID, 'android')
    _phone_overview_screen_locator = (By.ID, 'screen-overview')
    _phone_os_screen_locator = (By.ID, 'screen-os')
    _phone_marketplace_screen_locator = (By.ID, 'screen-marketplace')
    _android_phone_locator = (By.CLASS_NAME, 'android-phone-visible')

    @property
    def partner_menu(self):
        return self.PartnerMenu(self)

    @property
    def mwc_menu(self):
        return self.MWCMenu(self)

    @property
    def devices_menu(self):
        return self.DevicesMenu(self)

    @property
    def firefox_os(self):
        el = self.find_element(self._firefox_os_locator)
        return self.Article(self, root=el)

    @property
    def marketplace(self):
        el = self.find_element(self._marketplace_locator)
        return self.Article(self, root=el)

    @property
    def android(self):
        el = self.find_element(self._android_locator)
        return self.Article(self, root=el)

    @property
    def is_phone_overview_screen_displayed(self):
        return self.is_element_displayed(self._phone_overview_screen_locator)

    @property
    def is_phone_os_screen_displayed(self):
        return self.is_element_displayed(self._phone_os_screen_locator)

    @property
    def is_phone_marketplace_screen_displayed(self):
        return self.is_element_displayed(self._phone_marketplace_screen_locator)

    @property
    def is_android_phone_displayed(self):
        return self.is_element_displayed(self._android_phone_locator)

    class PartnerMenu(FirefoxBasePageRegion):

        _root_locator = (By.ID, 'partner-menu')
        _overview_locator = (By.ID, 'menu-overview')
        _firefox_os_locator = (By.ID, 'menu-os')
        _marketplace_locator = (By.ID, 'menu-marketplace')
        _android_locator = (By.ID, 'menu-android')

        def show_overview(self):
            el = self.find_element(self._overview_locator)
            item = self.MenuItem(self.page, root=el)
            item.click()
            self.wait.until(
                lambda s: self.page.is_phone_overview_screen_displayed)

        def show_firefox_os(self):
            el = self.find_element(self._firefox_os_locator)
            item = self.MenuItem(self.page, root=el)
            item.click()
            self.wait.until(lambda s: self.page.is_phone_os_screen_displayed)

        def show_marketplace(self):
            el = self.find_element(self._marketplace_locator)
            item = self.MenuItem(self.page, root=el)
            item.click()
            self.wait.until(
                lambda s: self.page.is_phone_marketplace_screen_displayed)

        def show_android(self):
            el = self.find_element(self._android_locator)
            item = self.MenuItem(self.page, root=el)
            item.click()
            self.wait.until(lambda s: self.page.is_android_phone_displayed)

        class MenuItem(FirefoxBasePageRegion):

            _link_locator = (By.TAG_NAME, 'a')

            @property
            def is_selected(self):
                return 'active' in self._root.get_attribute('class')

            def click(self):
                self.find_element(self._link_locator).click()
                self.wait.until(lambda s: self.is_selected)

    class MWCMenu(FirefoxBasePageRegion):

        _root_locator = (By.ID, 'mwc-menu')
        _map_locator = (By.ID, 'menu-mwc-map')
        _schedule_locator = (By.ID, 'menu-mwc-schedule')

        def show_map(self):
            modal = Modal(self)
            el = self.find_element(self._map_locator)
            self.MenuItem(self.page, root=el).click()
            self.wait.until(lambda s: modal.is_displayed)
            return modal

        def show_schedule(self):
            modal = Modal(self)
            el = self.find_element(self._schedule_locator)
            self.MenuItem(self.page, root=el).click()
            self.wait.until(lambda s: modal.is_displayed)
            return modal

        class MenuItem(FirefoxBasePageRegion):

            _link_locator = (By.TAG_NAME, 'a')

            def click(self):
                self.find_element(self._link_locator).click()

    class DevicesMenu(FirefoxBasePageRegion):

        _root_locator = (By.ID, 'devices-menu')
        _devices_locator = (By.ID, 'menu-devices')

        def show_devices(self):
            el = self.find_element(self._devices_locator)
            self.MenuItem(self.page, root=el).click()
            from pages.firefox.os.devices import DevicesPage
            return DevicesPage(self.base_url, self.selenium).wait_for_page_to_load()

        class MenuItem(FirefoxBasePageRegion):

            _link_locator = (By.TAG_NAME, 'a')

            def click(self):
                self.find_element(self._link_locator).click()

    class Article(FirefoxBasePageRegion):

        _menu_locator = (By.TAG_NAME, 'nav')
        _section_locator = (By.CSS_SELECTOR, 'section[data-current="1"]')

        @property
        def menu(self):
            el = self.find_element(self._menu_locator)
            return self.Menu(self.page, root=el)

        @property
        def section(self):
            el = self.find_element(self._section_locator)
            return el.get_attribute('id')

        class Menu(FirefoxBasePageRegion):

            _items_locator = (By.TAG_NAME, 'a')

            @property
            def items(self):
                els = self.find_elements(self._items_locator)
                return [self.MenuItem(self.page, root=el) for el in els]

            class MenuItem(FirefoxBasePageRegion):

                @property
                def id(self):
                    return self._root.get_attribute('data-section')

                def click(self):
                    self._root.click()
