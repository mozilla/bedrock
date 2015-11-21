# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pages.firefox.base import FirefoxBasePage, FirefoxBasePageRegion
from pages.regions.modal import Modal


class DevicesPage(FirefoxBasePage):

    _url = '{base_url}/{locale}/firefox/os/devices'

    _location_select_locator = (By.ID, 'location')
    _get_phone_button_locator = (By.CSS_SELECTOR, '.location-select-wrapper button')
    _phone_thumbnail_locator = (By.CSS_SELECTOR, '#smartphones li:first-child > .device-thumbnail')
    _phone_detail_locator = (By.CSS_SELECTOR, '.smartphone-detail-list .device-detail:first-child')
    _tv_thumbnail_locator = (By.CSS_SELECTOR, '#tvs li:first-child > .device-thumbnail')
    _tv_detail_locator = (By.CSS_SELECTOR, '.tvs-detail-list .device-detail:first-child')

    def select_location(self, value):
        el = self.find_element(self._location_select_locator)
        Select(el).select_by_visible_text(value)
        self.wait.until(lambda s: self.is_get_a_phone_enabled)

    @property
    def is_get_a_phone_enabled(self):
        return self.find_element(self._get_phone_button_locator).is_enabled()

    def get_a_phone(self):
        modal = Modal(self.base_url, self.selenium)
        self.find_element(self._get_phone_button_locator).click()
        self.wait.until(lambda s: modal.is_displayed)
        return modal

    def open_phone_detail(self):
        self.scroll_element_into_view(self._phone_thumbnail_locator).click()
        el = self.find_element(self._phone_detail_locator)
        detail = DeviceDetail(self.base_url, self.selenium, root=el)
        # wait until close button is displayed for detail pane to initialize
        self.wait.until(lambda s: detail.is_close_displayed)
        return detail

    def open_tv_detail(self):
        self.scroll_element_into_view(self._tv_thumbnail_locator).click()
        el = self.find_element(self._tv_detail_locator)
        detail = DeviceDetail(self.base_url, self.selenium, root=el)
        self.find_element(self._tv_thumbnail_locator).click()
        # wait until close button is displayed for detail pane to initialize
        self.wait.until(lambda s: detail.is_close_displayed)
        return detail


class DeviceDetail(FirefoxBasePageRegion):

    _detail_locator = (By.CSS_SELECTOR, '.container')
    _features_locator = (By.CSS_SELECTOR, '.features')
    _specifications_locator = (By.CSS_SELECTOR, '.specifications')
    _close_button_locator = (By.CSS_SELECTOR, '.device-detail-close')
    _features_link_locator = (By.CSS_SELECTOR, '.pager-tabs li:first-child > a')
    _specifications_link_locator = (By.CSS_SELECTOR, '.pager-tabs li:last-child > a')

    @property
    def is_displayed(self):
        return self.is_element_displayed(self._detail_locator)

    @property
    def is_features_displayed(self):
        return self.is_element_displayed(self._features_locator)

    @property
    def is_specifications_displayed(self):
        return self.is_element_displayed(self._specifications_locator)

    @property
    def is_close_displayed(self):
        return self.is_element_displayed(self._close_button_locator)

    def show_specifications(self):
        assert not self.is_specifications_displayed, 'Specifications tab is already displayed'
        self.scroll_element_into_view(self._specifications_link_locator).click()
        self.wait.until(lambda s: self.is_specifications_displayed)

    def show_features(self):
        assert not self.is_features_displayed, 'Features tab is already displayed'
        self.scroll_element_into_view(self._features_link_locator).click()
        self.wait.until(lambda s: self.is_features_displayed)

    def close(self):
        self.scroll_element_into_view(self._close_button_locator).click()
        self.wait.until(lambda s: not self.is_displayed)
