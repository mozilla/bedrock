# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.regions.modal import ModalProtocol


class LeadershipPage(BasePage):

    _URL_TEMPLATE = "/{locale}/about/leadership/"

    _bios_locator = (By.CSS_SELECTOR, ".gallery .vcard.has-bio")
    _modal_bio_locator = (By.CSS_SELECTOR, ".mzp-c-modal .vcard.has-bio")

    @property
    def corporation(self):
        leaders = self.find_elements(*self._bios_locator)
        return [leader.get_attribute("id") for leader in leaders]

    def open_biography(self, value):
        modal = ModalProtocol(self)
        self.find_element(*(By.ID, value)).click()
        self.wait.until(lambda s: modal.is_displayed)
        return modal

    def is_biography_displayed(self, value):
        return self.is_element_displayed(*(By.CSS_SELECTOR, f'.mzp-c-modal .vcard.has-bio[data-id="{value}"]'))
