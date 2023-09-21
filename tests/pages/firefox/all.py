# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pages.base import BasePage, BaseRegion


class FirefoxAllPage(BasePage):
    _URL_TEMPLATE = "/{locale}/firefox/all/"

    _product_locator = (By.ID, "select-product")
    _product_options_locator = (By.CLASS_NAME, "c-selection-options")
    _desktop_download_button_locator = (By.ID, "download-button-primary")
    _android_download_button_locator = (By.ID, "download-android-primary")
    _android_beta_download_button_locator = (By.ID, "download-android-beta-primary")
    _android_nightly_download_button_locator = (By.ID, "download-android-nightly-primary")
    _ios_download_button_locator = (By.ID, "download-ios-primary")
    _download_info_platform_locator = (By.ID, "download-info-platform")
    _download_info_language_locator = (By.ID, "download-info-language")

    @property
    def _options(self):
        return [ProductOptions(self, root=el) for el in self.find_elements(*self._product_options_locator)]

    @property
    def product(self):
        select = self.find_element(*self._product_locator)
        return select.get_attribute("value")

    @property
    def platform_info(self):
        platform = self.find_element(*self._download_info_platform_locator)
        return platform.text

    @property
    def language_info(self):
        language = self.find_element(*self._download_info_language_locator)
        return language.text

    @property
    def desktop_download_link(self):
        link = self.find_element(*self._desktop_download_button_locator)
        return link.get_attribute("href")

    @property
    def is_desktop_download_button_displayed(self):
        return self.is_element_displayed(*self._desktop_download_button_locator)

    def select_product(self, value):
        el = self.find_element(*self._product_locator)
        Select(el).select_by_visible_text(value)
        selected = self.product
        option = [o for o in self._options if selected == o.root.get_attribute("data-product")]
        assert len(option) == 1
        self.wait.until(lambda s: option[0].is_displayed)
        return option[0]

    @property
    def is_android_download_button_displayed(self):
        return self.is_element_displayed(*self._android_download_button_locator)

    @property
    def is_android_beta_download_button_displayed(self):
        return self.is_element_displayed(*self._android_beta_download_button_locator)

    @property
    def is_android_nightly_download_button_displayed(self):
        return self.is_element_displayed(*self._android_nightly_download_button_locator)

    @property
    def is_ios_download_button_displayed(self):
        return self.is_element_displayed(*self._ios_download_button_locator)


class ProductOptions(BaseRegion):
    _platform_locator = (By.CSS_SELECTOR, ".c-selection-platform select")
    _language_locator = (By.CSS_SELECTOR, ".c-selection-language select")

    @property
    def is_displayed(self):
        return self.root.is_displayed()

    @property
    def platform(self):
        select = self.find_element(*self._platform_locator)
        return select.get_attribute("value")

    def select_platform(self, value):
        el = self.find_element(*self._platform_locator)
        Select(el).select_by_visible_text(value)
        self.wait.until(lambda s: self.page.platform_info == value)

    @property
    def language(self):
        select = self.find_element(*self._language_locator)
        return select.get_attribute("value")

    def select_language(self, value):
        el = self.find_element(*self._language_locator)
        Select(el).select_by_visible_text(value)
        self.wait.until(lambda s: self.page.language_info == value)
