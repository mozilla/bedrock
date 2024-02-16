# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class ManifestoPage(BasePage):
    _URL_TEMPLATE = "/{locale}/about/manifesto/"

    _primary_share_button_locator = (By.CSS_SELECTOR, ".share-addendum .js-manifesto-share")
    _secondary_share_button_locator = (By.CSS_SELECTOR, ".principles-foot .js-manifesto-share")

    @property
    def is_primary_share_button_displayed(self):
        return self.is_element_displayed(*self._primary_share_button_locator)

    @property
    def is_secondary_share_button_displayed(self):
        return self.is_element_displayed(*self._secondary_share_button_locator)
