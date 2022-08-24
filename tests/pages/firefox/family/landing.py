# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class FamilyPage(BasePage):

    _URL_TEMPLATE = "/{locale}/firefox/family/"

    _firefox_download_button_locator = (By.CSS_SELECTOR, "[data-link-type='download']")

    _firefox_pdf_download_button_locator = (By.CSS_SELECTOR, "[data-cta-text='Download PDF']")

    @property
    def is_firefox_download_button_displayed(self):
        return self.is_element_displayed(*self._firefox_download_button_locator)

    @property
    def is_firefox_pdf_download_button_displayed(self):
        return self.is_element_displayed(*self._firefox_pdf_download_button_locator)
