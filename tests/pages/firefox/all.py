# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.regions.modal import ModalProtocol


class FirefoxAllPage(BasePage):
    _URL_TEMPLATE = "/{locale}/firefox/all/{slug}"

    _desktop_list_items_locator = (By.CSS_SELECTOR, ".qa-desktop-list li")
    _mobile_list_items_locator = (By.CSS_SELECTOR, ".qa-mobile-list li")
    _platform_list_items_locator = (By.CSS_SELECTOR, ".c-platform-list li")
    _desktop_download_button_locator = (By.ID, "download-button-primary")
    _android_download_button_locator = (By.ID, "playStoreLink")
    _ios_download_button_locator = (By.ID, "appStoreLink")
    _ms_store_download_button_locator = (By.ID, "msStoreLink")
    _linux_atp_link_locator = (By.CSS_SELECTOR, ".c-linux-debian a")
    _back_icons_locator = (By.CSS_SELECTOR, "[src='/media/protocol/img/icons/close.svg']")

    # product

    @property
    def desktop_product_list_length(self):
        list = self.find_elements(*self._desktop_list_items_locator)
        return len(list)

    @property
    def mobile_product_list_length(self):
        list = self.find_elements(*self._mobile_list_items_locator)
        return len(list)

    # platform

    @property
    def platform_list_length(self):
        list = self.find_elements(*self._platform_list_items_locator)
        return len(list)

    # language

    # downloads

    @property
    def is_desktop_download_button_displayed(self):
        return self.is_element_displayed(*self._desktop_download_button_locator)

    @property
    def desktop_download_link(self):
        link = self.find_element(*self._desktop_download_button_locator)
        return link.get_attribute("href")

    @property
    def is_android_download_button_displayed(self):
        return self.is_element_displayed(*self._android_download_button_locator)

    @property
    def is_ios_download_button_displayed(self):
        return self.is_element_displayed(*self._ios_download_button_locator)

    @property
    def microsoft_store_link(self):
        link = self.find_element(*self._ms_store_download_button_locator)
        return link.get_attribute("href")

    @property
    def is_ms_store_download_button_displayed(self):
        return self.is_element_displayed(*self._ms_store_download_button_locator)

    @property
    def linux_atp_link(self):
        link = self.find_element(*self._linux_atp_link_locator)
        return link.get_attribute("href")

    @property
    def is_linux_atp_link_displayed(self):
        return self.is_element_displayed(*self._linux_atp_link_locator)

    # back buttons

    @property
    def back_icons_count(self):
        list = self.find_elements(*self._back_icons_locator)
        return len(list)

    # help modals

    def open_help_modal(self, value):
        modal = ModalProtocol(self)
        self.find_element(*(By.ID, value)).click()
        self.wait.until(lambda s: modal.is_displayed)
        return modal

    def is_help_modal_displayed(self, value):
        return self.is_element_displayed(*(By.CSS_SELECTOR, f'.mzp-c-modal .vcard.has-bio[data-id="{value}"]'))
