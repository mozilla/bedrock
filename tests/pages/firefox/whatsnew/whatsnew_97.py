# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.regions.modal import ModalProtocol


class FirefoxWhatsNew97Page(BasePage):

    _URL_TEMPLATE = "/{locale}/firefox/97.0/whatsnew/"

    _pocket_button_locator = (By.CSS_SELECTOR, ".wnp-main-cta .mzp-c-button")
    _modal_button_locator = (By.CSS_SELECTOR, ".wnp-main-cta .js-video-play")

    @property
    def is_pocket_button_displayed(self):
        return self.is_element_displayed(*self._pocket_button_locator)

    @property
    def is_modal_button_displayed(self):
        return self.is_element_displayed(*self._modal_button_locator)

    def open_modal(self, locator):
        modal = ModalProtocol(self)
        self.find_element(*locator).click()
        self.wait.until(lambda s: modal.is_displayed)
        return modal

    def click_modal_button(self):
        self.scroll_element_into_view(*self._modal_button_locator)
        return self.open_modal(self._modal_button_locator)
