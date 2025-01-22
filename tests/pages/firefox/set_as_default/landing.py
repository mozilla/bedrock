# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class DefaultLandingPage(BasePage):
    _URL_TEMPLATE = "/{locale}/firefox/set-as-default/"

    _set_default_button_locator = (By.ID, "set-as-default-button")

    @property
    def is_set_default_button_displayed(self):
        return self.is_element_displayed(*self._set_default_button_locator)
