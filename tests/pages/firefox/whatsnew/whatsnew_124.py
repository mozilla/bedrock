# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected

from pages.base import BasePage
from pages.regions.modal import ModalProtocol


class FirefoxWhatsNew124Page(BasePage):
    _URL_TEMPLATE = "/{locale}/firefox/124.0/whatsnew/{params}"

    _monitor_free_scan_button_locator = (By.CSS_SELECTOR, '.wnp-main-cta[data-cta-text="Start with a free scan"]')
    _set_as_default_button_locator = (By.CSS_SELECTOR, ".wnp-main-cta.is-not-default")
    _youtube_channel_button_locator = (By.CSS_SELECTOR, '.wnp-main-cta[data-cta-text="Das ganze Video auf YouTube"]')
    _share_modal_button_locator = (By.CSS_SELECTOR, ".wnp-main-cta.js-modal-link")
    _share_copy_button_locator = (By.ID, "copy-button")

    @property
    def is_monitor_free_scan_button_displayed(self):
        return self.is_element_displayed(*self._monitor_free_scan_button_locator)

    @property
    def is_set_as_default_button_displayed(self):
        self.wait.until(expected.visibility_of_element_located(self._set_as_default_button_locator))
        return self.is_element_displayed(*self._set_as_default_button_locator)

    @property
    def is_youtube_channel_button_displayed(self):
        return self.is_element_displayed(*self._youtube_channel_button_locator)

    @property
    def is_share_copy_button_displayed(self):
        return self.is_element_displayed(*self._share_copy_button_locator)

    def open_share_modal(self):
        modal = ModalProtocol(self)
        self.find_element(*self._share_modal_button_locator).click()
        self.wait.until(lambda s: modal.displays(self._share_copy_button_locator))
        return modal
